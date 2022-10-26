import logging
import sys
from collections.abc import Generator, Iterable
from dataclasses import dataclass
from typing import Union, Optional

from bs4 import BeautifulSoup, ResultSet, Tag
from pydantic import BaseModel, Field
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.chromium.webdriver import ChromiumDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

__all__ = ['MethodDoc', 'SectionDoc', 'AttributeInfo', 'Parameter', 'MethodDetails', 'DocMethodDetails',
           'DevWebexComScraper']

# menu titles we want to pull method details from
from yaml import safe_load, safe_dump

TARGET_MENUS = {
    'Call Controls',
    'Locations',
    'Webex Calling Organization Settings',
    'Webex Calling Person Settings',
    'Webex Calling Voice Messaging',
    'Webex Calling Workspace Settings with Numbers'
}


def debugger() -> bool:
    """
    Check if executed in debugger
    """
    return (gt := getattr(sys, 'gettrace', None)) and gt()


def div_repr(d) -> str:
    """
    Simple text representation of a div
    """
    if d is None:
        return 'None'
    assert d.name == 'div'
    classes = d.attrs.get('class', None)
    if classes:
        class_str = f" class={' '.join(classes)}"
    else:
        class_str = ''
    return f'<div{class_str}>'


class MethodDoc(BaseModel):
    #: HTTP method
    method: str
    #: API endpoint URL
    endpoint: str
    #: link to documentation page
    doc_link: str
    #: Documentation
    doc: str


class SectionDoc(BaseModel):
    """
    Available documentation for one section on developer.webex.com

    For example for Calling/Reference/Locations
    """
    #: menu text at top of page
    menu_text: str
    #: list of methods parsed from the page
    methods: list[MethodDoc]


@dataclass
class AttributeInfo:
    path: str
    parameter: 'Parameter'


class Parameter(BaseModel):
    name: str
    type: str
    type_spec: Optional[str]
    doc: str
    # parsed from params-type-non-object: probably an enum
    param_attrs: Optional[list['Parameter']]
    # parsed from params-type-object: child object
    param_object: Optional[list['Parameter']]

    def attributes(self, *, path: str) -> Generator[AttributeInfo, None, None]:
        yield AttributeInfo(parameter=self, path=f'{path}/{self.name}')
        for p in self.param_attrs or list():
            yield from p.attributes(path=f'{path}/{self.name}/attrs')
        for p in self.param_object or list():
            yield from p.attributes(path=f'{path}/{self.name}/object')


class MethodDetails(BaseModel):
    header: str
    doc: str
    parameters_and_response: dict[str, list[Parameter]]
    documentation: MethodDoc

    def attributes(self, *, path: str) -> Generator[AttributeInfo, None, None]:
        for pr_key in self.parameters_and_response:
            for p in self.parameters_and_response[pr_key]:
                yield from p.attributes(path=f'{path}/{self.header}/{pr_key}')


class DocMethodDetails(BaseModel):
    """
    Container for all information; interface to YML file
    """
    docs: dict[str, list[MethodDetails]] = Field(default_factory=dict)

    @staticmethod
    def from_yml(path: str):
        with open(path, mode='r') as f:
            return DocMethodDetails.parse_obj(safe_load(f))

    def to_yml(self, path: Optional[str] = None) -> Optional[str]:
        data = self.dict()
        if path:
            with open(path, mode='w') as f:
                safe_dump(data, f)
            return None
        else:
            return safe_dump(data)

    def methods(self) -> Generator[MethodDetails, None, None]:
        for method_details in self.docs.values():
            yield from method_details

    def attributes(self) -> Generator[AttributeInfo, None, None]:
        for method_details_key in self.docs:
            method_details = self.docs[method_details_key]
            for md in method_details:
                yield from md.attributes(path=f'{method_details_key}')


@dataclass
class DevWebexComScraper:
    driver: ChromiumDriver
    logger: logging.Logger

    def __init__(self):
        self.driver = webdriver.Chrome()
        self.logger = logging.getLogger(f'{__name__}.{self.__class__.__name__}')

    def close(self):
        self.log('close()')
        if self.driver:
            self.driver.quit()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.log('__exit__()')
        self.close()

    def __enter__(self):
        return self

    def log(self, msg: str, level: int = logging.DEBUG):
        self.logger.log(level=level, msg=msg)

    @staticmethod
    def by_class_and_text(find_in: Union[ChromiumDriver, WebElement], class_name: str, text: str) -> WebElement:
        """
        Find a WebElement by class name and text

        :param find_in: root to search in
        :param class_name: class name
        :param text: text
        :return: WebElement
        :raises:
            StopIteration: if no element can be found
        """
        return next((element for element in find_in.find_elements(by=By.CLASS_NAME, value=class_name)
                     if element.text == text))

    def methods_from_api_reference_container(self, container: BeautifulSoup,
                                             header: str) -> Generator[MethodDoc, None, None]:
        """
        Yield method documentation instances for each method parsed from an API reference container on the right

        Container looks like:
            <div class="api_reference_entry__container">
                <div class="columns large-9">
                    <div class="XZCMfprZP3RvdJJ_CfTH"><h3>Locations</h3>
                        <p>Locations are used to organize Webex Calling (BroadCloud) features within physical
                        locations. Y .... .</p></div>
                    <div>
                        <div class="clearfix dVWBljZUFIGiEgkvpTg5"><h5 class="columns
                        small-9"><span>Method</span></h5><h5
                                class="columns small-3"><span>Description</span></h5></div>
                        <div class="UuvKF2Qey4J1ajkvpmiN">
                            <div class="B_af0kjJ65j92iCwAiw1">
                                <div class="columns small-9"><span
                                        class="md-badge md-badge--green E38yq9G_nWIm8SdrG1GU">GET</span><span
                                        class="X9_XSxV8TI6eNf98ElQU"><a
                                        href="/docs/api/v1/locations/list-locations">https://webexapis.com/v1
                                        /locations</a></span>
                                </div>
                                <div class="columns small-3 sn1OrZrRvd9GVOvUv4WK">List Locations</div>
                            </div>
                            <div class="cg3iKW8BWwV8ooZrsjQi">
                                <div class="X9_XSxV8TI6eNf98ElQU"><a
                                href="/docs/api/v1/locations/list-locations">https://webexapis.com/v1/locations</a>
                                </div>
                                <span class="md-badge md-badge--green E38yq9G_nWIm8SdrG1GU">GET</span><span
                                    class="sn1OrZrRvd9GVOvUv4WK">List Locations</span></div>
                        </div>

        :param container: API reference container
        :param header: header these methods belong under; for logging
        """

        def log(text: str, level: int = logging.DEBUG):
            self.log(f'    methods_from_api_reference_container("{header}"): {text}',
                     level=level)

        log('start')
        rows = container.div.div.find_all('div', recursive=False)[1].find_all('div', recursive=False)
        """
            Rows look like this:
                <div class="B_af0kjJ65j92iCwAiw1">
                    <div class="columns small-9"><span class="md-badge md-badge--green 
                    E38yq9G_nWIm8SdrG1GU">GET</span><span
                            class="X9_XSxV8TI6eNf98ElQU"><a
                            href="/docs/api/v1/broadworks-billing-reports/list-broadworks-billing-reports">https
                            ://webexapis.com/v1/broadworks/billing/reports</a></span>
                    </div>
                    <div class="columns small-3 sn1OrZrRvd9GVOvUv4WK">List BroadWorks Billing Reports</div>
                </div>
                <div class="cg3iKW8BWwV8ooZrsjQi">
                    <div class="X9_XSxV8TI6eNf98ElQU"><a 
                    href="/docs/api/v1/broadworks-billing-reports/list-broadworks-billing-reports">https://webexapis
                    .com/v1/broadworks/billing/reports</a>
                    </div>
                    <span class="md-badge md-badge--green E38yq9G_nWIm8SdrG1GU">GET</span><span 
                    class="sn1OrZrRvd9GVOvUv4WK">List BroadWorks Billing Reports</span>
                </div>
        """
        for soup_row in rows[1:]:
            method = soup_row.div.div.span.text
            endpoint = soup_row.div.div.a.text
            doc_link = f"https://developer.webex.com{soup_row.div.div.a.get('href')}"
            doc = soup_row.div.find_all('div')[1].text

            log(f'{doc}', level=logging.INFO)
            log(f'yield: {method} {endpoint}: {doc}, {doc_link}', level=logging.DEBUG)
            yield MethodDoc(method=method, endpoint=endpoint, doc_link=doc_link, doc=doc)
        log('end')

    def docs_from_submenu_items(self, submenus: list[WebElement]) -> Generator[SectionDoc, None, None]:
        """
        Yield section information for each submenu on the left
        :param submenus:
        :return:
        """

        def log(text: str, level: int = logging.DEBUG):
            self.log(f'  endpoints_from_submenu_items({submenu.text}): {text}',
                     level=level)

        prev_container_header = None

        def wait_for_new_api_reference_container():
            """
            Wait until the page on teh right has been updated with new content after clicking on a new section on the
            left
            """

            def log(text: str):
                self.log(f'  wait_for_new_api_reference_container: {text}')

            def _predicate(driver):
                """
                Look for API reference container and check if the container header has changed
                """
                target = driver.find_element(By.CLASS_NAME, 'api_reference_entry__container')
                log('Container found' if target else 'Container not found')
                target = EC.visibility_of(target)(driver)
                log(f'Visibility: {not not target}')
                if target:
                    target: WebElement
                    # header selector: div.api_reference_entry__container > div > div:nth-of-type(1) > h3
                    container_header = target.find_element(
                        by=By.CSS_SELECTOR,
                        value='div > div:nth-of-type(1) > h3')

                    log(f'prev container header: {prev_container_header}, header: {container_header.text}')
                    if container_header.text != prev_container_header:
                        return target, container_header.text
                return False

            return _predicate

        for submenu in submenus:
            if submenu.text not in TARGET_MENUS:
                log(f'skipping')
                continue

            log(f'Extracting methods from "{submenu.text}" menu', level=logging.INFO)

            log('start')
            log('click()')

            # click on the submenu on the left
            submenu.click()

            # after clicking on the submenu we need to wait for a new api reference container to show up
            api_reference_container, header = WebDriverWait(driver=self.driver, timeout=10).until(
                method=wait_for_new_api_reference_container())
            api_reference_container: WebElement
            header: str

            # set the new header (needed when waiting for the next container)
            prev_container_header = header

            soup = BeautifulSoup(api_reference_container.get_attribute('outerHTML'), 'html.parser')
            yield SectionDoc(menu_text=submenu.text,
                             methods=list(self.methods_from_api_reference_container(
                                 container=soup,
                                 header=header)))
            log('end')
        return

    def get_calling_docs(self) -> list[SectionDoc]:
        """
        Read developer.webex.com and get doc information for all endpoints under "Calling"
        """
        url = 'https://developer.webex.com/docs'

        def log(text: str, level: int = logging.DEBUG):
            self.log(level=level, msg=f'navigate_to_calling_reference: {text}')

        log(f'opening "{url}"')
        self.driver.get(url)

        # wait max 10 seconds for accept cookies button to show up and be steady

        log('waiting for button to accept cookies')

        def steady(locator):
            """
            Wait for a web element to be:
                * visible
                * enabled
                * steady: same position at two consecutive polls
            :param locator:
            :return: False or web element
            """
            #: mutable to cache postion of element
            mutable = {'pos': dict()}

            def log(text: str):
                self.log(f'steady: {text}')

            def _predicate(driver):
                target = driver.find_element(*locator)
                target = EC.visibility_of(target)(driver)
                if target and target.is_enabled():
                    target: WebElement
                    pos = target.location
                    log(f'prev pos: {mutable["pos"]}, pos: {pos}')
                    if mutable['pos'] == pos:
                        return target
                    mutable['pos'] = pos
                else:
                    log(f'not visible or not enabled')
                return False

            return _predicate

        try:
            # wait for button to accept cookies to be steady
            accept_cookies = WebDriverWait(driver=self.driver, timeout=10).until(
                method=steady((By.ID, 'onetrust-accept-btn-handler')))
        except TimeoutException:
            # if there is no accept cookies button after 10 seconds then we are probably ok
            log('No popup to accept cookies', level=logging.WARNING)
        else:
            accept_cookies: WebElement
            log('accept cookies')
            accept_cookies.click()

        log('looking for "Calling"')
        calling = self.by_class_and_text(find_in=self.driver,
                                         class_name='md-list-item__center',
                                         text='Calling')
        log('clicking on "Calling"')
        calling.click()

        # after clicking on "Calling" an expanded nav group exists
        log('looking for expanded sidebar nav group')
        calling_nav_group = self.driver.find_element(by=By.CLASS_NAME, value='md-sidebar-nav__group--expanded')

        # in that nav group we want to click on "Reference"
        log('looking for "Reference" in expanded sidebar group')
        reference = self.by_class_and_text(find_in=calling_nav_group,
                                           class_name='md-list-item__center',
                                           text='Reference')
        log('clicking on "Reference"')
        reference.click()

        # After clicking on "Reference" a new expanded nav group should exist
        log('Looking for expanded sidebar nav group under "Calling"')
        reference_nav_group = next(iter(calling_nav_group.find_elements(by=By.CLASS_NAME,
                                                                        value='md-sidebar-nav__group--expanded')))
        log('Collecting menu items in "Reference" sidebar group')
        reference_items = reference_nav_group.find_elements(by=By.CLASS_NAME, value='md-submenu__item')
        log(f"""menu items in "Reference" sidebar group: {', '.join(f'"{smi.text}"' for smi in reference_items)}""")

        docs = list(self.docs_from_submenu_items(reference_items))
        return docs

    def param_parser(self, divs: Iterable[Tag], level: int = 0) -> Generator[Parameter, None, None]:
        """
        Parse parameters from divs
        :param divs:
        :return:
        """

        param_div = None
        name = None

        def log(msg: str, div: Tag = None):
            div = div or param_div
            name_str = name and f'"{name}", ' or ""
            self.log(f'      {"  " * level}param_parser({div_repr(div)}): {name_str}{msg}')

        def next_div() -> Optional[Tag]:
            div = next(div_iter, None)
            log(f'next param div', div)
            return div

        log(f'start: divs({len(divs)}): {", ".join(map(div_repr, divs))}')
        div_iter = iter(divs)
        param_div = next_div()
        while param_div:
            name = None
            if param_div.attrs.get('class', None) is None:
                # yield members of classless div
                yield from self.param_parser(param_div.find_all('div', recursive=False),
                                             level=level)
                # and then continue with the next
                param_div = next_div()
                continue

            # if this div only has one div child then go one down
            # for a parameter we expect two child divs
            if len(param_div.find_all('div', recursive=False)) == 1:
                param_div = param_div.div
                log('div with single div child. moved one down')

            # special case: a div w/o child divs and just two spans
            if not param_div.find_all('div', recursive=False):
                spans = param_div.find_all('span', recursive=False)
                if len(spans) == 2:
                    yield Parameter(name=spans[0].text,
                                    type='',
                                    doc=f'{spans[0].text}{spans[1].text}')
                param_div = next_div()
                continue

            # if there is a button then go one down
            if param_div.button:
                param_div = param_div.div
                log(f'found a button, went one down')

            param_attrs = None
            param_object = None

            # the div should have two child divs:
            #   * attribute name and type
            #   * attribute doc string
            child_divs = param_div.find_all('div', recursive=False)
            log(f'child divs({len(child_divs)}): {", ".join(map(div_repr, child_divs))}')

            if len(child_divs) == 2:
                """
                Parse something like this
                    <div class="bfIcOqrr0LEmWxjEID2z">
                        <div class="ETdjpkOd18yDmr_Pomer">
                            <div class="AzemgtvlBWwLVUYkRkbg">personId</div>
                            <div class="Xjm2mpYxY4YHNn4XsTBg"><span>string</span><span 
                            class="buEuRUqtw7z8xim5DxxA">required</span></div>
                        </div>
                        <div class="Sj3x8PGVKM_DQu1MaOpF"><p>Unique identifier for the person.</p></div>
                    </div>
                """
                param_div, p_spec_div = child_divs

                # get attribute name and type
                child_divs = param_div.find_all('div', recursive=False)
                log(f'param child divs({len(child_divs)}): {", ".join(map(div_repr, child_divs))}')
                assert len(child_divs) == 2
                name_div, type_div = child_divs
                name = name_div.text

                # type information has type and addtl. spec in spans
                spans = type_div.find_all('span', recursive=False)
                log(f'# of spans in type spec: {len(spans)}')
                assert len(spans) and len(spans) <= 2
                param_type = spans[0].text
                if len(spans) == 2:
                    type_spec = spans[1].text
                else:
                    type_spec = None

                # doc is in the second div
                doc_paragraphs = p_spec_div.find_all('p', recursive=False)
                doc = '\n'.join(map(lambda p: p.text, doc_paragraphs))

                # for an enum the second div can have a list of enum values
                child_divs = p_spec_div.find_all('div', recursive=False)
                if child_divs:
                    log(f'divs in second div of parameter parsed ({len(child_divs)}): '
                        f'{", ".join(map(div_repr, child_divs))}')
                    param_attrs = list(self.param_parser(child_divs, level=level + 1)) or None
            elif len(child_divs) < 3:
                # to short: not idea what we can do here....
                log(f'to few divs: {len(child_divs)}: skipping')
                param_div = next_div()
                continue
            else:
                """
                Special case:
                    <div class="emjDUw5LqTp3QCCg4hNp">
                        <div class="AzemgtvlBWwLVUYkRkbg">primary</div>
                        <div class="Xjm2mpYxY4YHNn4XsTBg"><span>boolean</span></div>
                        <div class="Sj3x8PGVKM_DQu1MaOpF"><p>Flag to indicate if the number is primary or 
                        not.</p></div>
                        <div class="Mo4RauPOboRxtDGO9VvT"><span>Possible values: </span><span></span></div>
                    </div>      
                """
                childs = iter(child_divs)
                name = next(childs).text
                log(f'flat sequence of divs')

                spans = iter(next(childs).find_all('span', recursive=False))
                param_type = next(spans).text
                span = next(spans, None)
                type_spec = span and span.text

                doc = '\n'.join(p.text
                                for p in next(childs).find_all('p', recursive=False))
                div = next(childs, None)
                if div:
                    spans = iter(div.find_all('span', recursive=False))
                    doc_line = f'{next(spans).text}{", ".join(t for s in spans if (t := s.text))}'
                    log(f'enhancing doc string: "{doc_line}"')
                    doc = '\n'.join((doc, doc_line))

            # if

            # look ahead to next div
            param_div = next_div()
            if param_div:
                # check if class is one of the param classes
                classes = set(param_div.attrs.get('class', []))
                if object_class := classes & {'params-type-non-object', 'params-type-object'}:
                    log(f'parsing next div ({next(iter(object_class))}) as part of this parameter')
                    # this enhances the current parameter
                    obj_attributes = list(self.param_parser(param_div.find_all('div', recursive=False),
                                                            level=level + 1)) or None
                    if 'params-type-non-object' in classes:
                        assert param_attrs is None
                        param_attrs = obj_attributes
                    else:
                        param_object = obj_attributes
                    # move to next div
                    param_div = next_div()
                # if
            # if
            log(f'yield type={param_type}, type_spec={type_spec}, '
                f'param_attrs={param_attrs and len(param_attrs) or 0}, '
                f'param_object={param_object and len(param_object) or 0}')
            yield Parameter(name=name,
                            type=param_type,
                            type_spec=type_spec,
                            doc=doc,
                            param_attrs=param_attrs,
                            param_object=param_object)
        # while
        return

    def params_and_response_from_divs(self, divs: ResultSet) -> dict[str, list[Parameter]]:
        """
        Extract params and response properties from child divs of api-reference__description
        :param divs:
        :return:
        """

        def log(msg: str):
            self.log(f'    params_and_response_from_divs: {msg}')

        log('start')
        result: dict[str, list[Parameter]] = {}
        for div in divs:
            # each div has one or more h6 headers and the same number of divs of class vertical-up with the parameter
            # information
            if div.attrs.get('class', None) is None:
                # navigate one level down if encapsulated in an empty div: this is the case for "Response Properties"
                div = div.div
                log(f'navigating one level down from <div> to {div_repr(div)}')
                if div is None:
                    # apparently this was an empty div; we are done here
                    continue
            headers = div.find_all(name='h6', recursive=False)
            parameter_groups = div.find_all(class_='vertical-up', recursive=False)
            assert len(headers) == len(parameter_groups)
            log(f"""{div_repr(div)}: headers({len(headers)}): {", ".join(map(lambda h: f'"{h.text}"', headers))}""")

            for header, parameters in zip(headers, parameter_groups):
                if False and debugger() and header.text != 'Response Properties':
                    continue
                # each parameter spec is in one child div
                child_divs = parameters.find_all(name='div', recursive=False)
                log(f'{div_repr(div)}, header("{header.text}"). child divs({len(child_divs)}): '
                    f'{", ".join(map(div_repr, child_divs))}')
                # parsed_params = list(map(self.parse_param, child_divs))
                parsed_params = list(self.param_parser(child_divs))
                result[header.text] = parsed_params
        log('end')
        return result

    def get_method_details(self, method_doc: MethodDoc) -> Optional[MethodDetails]:
        """
        Get details for one method

        :param method_doc:
        :return:
        """

        def log(msg: str, level: int = logging.DEBUG):
            self.log(f'  get_method_details("{method_doc.doc}"): {msg}',
                     level=level)

        if False and debugger() and method_doc.doc != 'Configure a person\'s Privacy Settings':
            # skip
            return

        log('', level=logging.INFO)

        doc_link = method_doc.doc_link
        # sometimes links have a superfluous trailing dot
        # we try the original URL 1st and retry w/p trailing dots
        while True:
            # navigate to doc url of method
            log(f'GET {doc_link}')
            self.driver.get(doc_link)

            # we don't need to click on anything. Hence we can just extract from static page using BeautifulSoup
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')

            api_ref_descr = soup.find(class_='api-reference__description')
            """ API reference description is something like:
                    <div class="columns u_6eoYxPfVMJxwlI0Wcb large-6 xlarge-6 api-reference__description 
                    XdQBFUuam5J29sqNCtir">
                        <div class="K_M3cdOQTnTLnPOWhtqe"><h4>Read Person's Calling Behavior</h4>
                            <div><p>Retrieves the calling behavior and UC Manager Profile settings for the person which 
                            includes overall
                                calling behavior and calling UC Manager Profile ID.</p>
                                <p>Webex Calling Behavior controls which Webex telephony application and which UC 
                                Manager 
                                Profile is to be
                                    used for a person.</p>
                                </div>
            """
            if not api_ref_descr:
                if doc_link.endswith('.'):
                    log(f'GET {doc_link} failed. Retry w/o trailing "."',
                        level=logging.WARNING)
                    doc_link = doc_link.strip('.')
                    continue
                log(f'GET failed? API reference description not found on page', level=logging.ERROR)
                return None
            break
        # while

        try:
            header = api_ref_descr.div.h4.text
        except AttributeError:
            log(f'Failed o parse header from api spec',
                level=logging.ERROR)
            return None

        log(f'header from API reference description: "{header}"')

        # long doc string can have multiple paragraphs
        doc_paragraphs = api_ref_descr.div.div.find_all(name='p', recursive=False)
        assert doc_paragraphs
        long_doc_string = '\n'.join(dp.text for dp in doc_paragraphs)

        # parameters and response values are in the divs following the 1st one. The last div has response codes
        # hence to get parameters and response codes we can skip the 1st and last div
        divs = api_ref_descr.find_all(name='div', recursive=False)

        divs = divs[1:-1]

        log(f'child divs for parameters and response: {", ".join(map(div_repr, divs))}')
        params_and_response = self.params_and_response_from_divs(divs)
        result = MethodDetails(header=header,
                               doc=long_doc_string,
                               parameters_and_response=params_and_response,
                               documentation=method_doc)
        log('end')
        return result
