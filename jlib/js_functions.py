import sys
sys.dont_write_bytecode = True

#functions excutes javascript on browser (page)
 
def log(msg):
    print(msg,end='\n')

def execute_script(page,script:str, arg=None):
    try:
        if arg is None:
            result = page.execute_script(script)
        else:
            result = page.execute_script(script,arg)
        return result
    except:
        pass


def is_page_loaded(page):
    try:
        state = page.execute_script('return document.readyState;')
        if state == 'complete':
            return True
        else:
            page.execute_script('setTimeout(arguments.callee, 100);')
            return False
    except:
        log("Failed to Load this page.")
        return False


def remove_element_by_selector(page,selector):
    try:
        page.execute_script(f"const element = document.querySelector('{selector}'); if (element) {{ element.remove(); }}")
    except:
        pass

def remove_elements_by_class_name(page, className:str):
    try:
        script = f"""
        var xElements = document.querySelectorAll('[class*="{className}"]');
        for (var i = 0; i < xElements.length; ++i) {{
        var ad = xElements[i];
        ad.style.display = "none";
        ad.innerHTML = "";}}"""
        page.execute_script(script)
    except:
        pass


def get_element_by_id(page,element_id):
    script = f"return document.getElementById('{element_id}');"
    element = page.execute_script(script)
    if element is None:
        raise Exception(f"No element found with ID '{element_id}'")
    return element


def get_elements_by_css_selector(page, selector:str):
    try:
        return page.execute_script(f'return document.querySelectorAll("{selector}")')
    except:
        return None



def get_element_by_css_selector(page, selector: str):
    try:
        return page.execute_script(f'return document.querySelector("{selector}")')
    except:
        return None
        


def get_element_by_xpath(page, xpath: str):
    try:
        elem = page.execute_script(f'return document.evaluate("{xpath}", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue')
        return elem
    except:
        return None


def get_elements_by_xpath(page, xpath: str):
    try:
        return page.execute_script(f'return document.evaluate("{xpath}", document, null, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null)')
    except:
        pass


def switch_to_iframe_by_css_selector(page, selector: str):
    try:
        iframe = get_element_by_css_selector(page,selector)
        page.execute_script('arguments[0].contentWindow.document', iframe)
        page.switch_to.frame(iframe)
    except:
        pass


def switch_to_iframe_by_xpath( page,xpath: str):
        try:
            iframe = get_element_by_xpath(page,xpath)
            page.execute_script('arguments[0].contentWindow.document', iframe)
            page.switch_to.frame(iframe)
        except:
            pass


def switch_to_default_content(page):
    page.switch_to.default_content()


def click_element_by_css_selector(page, selector: str):
    try:
        element = get_element_by_css_selector(page,selector)
        element.click()
        return True
    except:
        return False
    
def get_elements_from_element(page, parent_element, selector):
    try:
        if parent_element is None:
            return
            #raise ValueError("Parent element is None")
        #Use JavaScript to find child elements matching the CSS selector
        child_elements = page.execute_script(f"return arguments[0].querySelectorAll('{selector}');", parent_element)
        if child_elements is None:
            return
            #raise ValueError("No elements found for selector")
        return child_elements
    except Exception as ex:
        log(str(ex))
        return []


def get_element_from_element(page,parent_element, selector):
    try:
        if parent_element is None:
            return None
            #raise ValueError("Parent element is None")
        #Use JavaScript to find child elements matching the CSS selector
        child_element = page.execute_script(f"return arguments[0].querySelector('{selector}');", parent_element)
        if child_element is None:
            return None
            #raise ValueError("No element found for selector")
        return child_element
    except Exception as ex:
        log(str(ex))
        return None


def get_current_url(page):
    return page.execute_script('return window.location.href')

 #try_accept_alert
def try_accept_alert(page):
    try:
        page.execute_script('alert().accept();')
    except:
        pass


def send_string_to_element(page, element, text):
    try:
        page.execute_script("arguments[0].value = arguments[1];", element, text)
    except Exception as e:
        log(f"Error sending keys: {e}")

def append_string_to_element(page, element, text):
    try:
        page.execute_script("arguments[0].value += arguments[1];", element, text)
    except Exception as e:
        log(f"Error sending keys: {e}")

def send_string_to_element_char_by_char(page, element, text):
    try:
        for letter in text:
            page.execute_script("arguments[0].value += arguments[1];", element, letter)
    except Exception as e:
        log(f"Error sending keys: {e}")

def send_enter_key_to_element(page,element):
    try:
        # Send the "Return/Enter" key press event to the element
        page.execute_script("arguments[0].dispatchEvent(new KeyboardEvent('keydown',{'keyCode':13,'which':13}));", element)
        page.execute_script("arguments[0].dispatchEvent(new KeyboardEvent('keyup',{'keyCode':13,'which':13}));", element)
    except:
        log("Error sending Enter key to element.")


def send_enter_key(page):
    try:
        #Find the active element on the page
        active_element = page.execute_script("return document.activeElement;")
        send_enter_key_to_element(page,active_element)
    except:
        log("Error finding the active element.")

def get_url_from_element(page, element):
    try:
        return page.execute_script("return arguments[0].querySelector('a').getAttribute('href')", element)
    except:
        return None



def get_attribute_from_element(page, element,attribute):
    try:
        return page.execute_script(f"return arguments[0].getAttribute('{attribute}')", element)
    except:
        return None


def get_urls_in_elements(page, elements):
    try:
        urls = page.execute_script("""
            var elements = arguments[0];
            var urls = [];
            for (var i = 0; i < elements.length; ++i) {
                var a = elements[i].querySelector('a');
                if (a !== null) {
                    var url = a.getAttribute('href');
                    if (url !== null) {
                        urls.push(url);
                    }
                }
            }
            return urls;""", elements)
        return urls
    except Exception as e:
        raise Exception("Failed to extract URLs from elements: " + str(e))


def get_scroll_height(page):
    return page.execute_script("return document.body.scrollHeight")


def get_current_scroll_height(page):
    return page.execute_script("return window.pageYOffset")


def scroll_down_by_value(page,scroll_value):
    try:
        page.execute_script(f"window.scrollBy(0, {scroll_value});")
    except:
        log("Error scrolling down by value.")
    
def get_current_cookies(page):
    try:
        return page.execute_script("return document.cookie")
    except:
        log("Error getting current cookies.")


def replace_cookies_by(page,cookies):
    try:
        page.execute_script("document.cookie = ''")
        for cookie in cookies:
            page.execute_script(f"document.cookie = '{cookie['name']}={cookie['value']}; domain={cookie['domain']}; path={cookie['path']}; expires={cookie['expiry']}'")
    except:
        log("Error setting cookies.")


def render_element_to_page(page,html: str):
    try:
        script = "document.body.insertAdjacentHTML('beforeend', arguments[0]);"
        page.execute_script(script, html)
    except Exception as e:
        log(f"Error rendering element to page: {str(e)}")


def replace_element_with_html_string(page, selector: str, new_html_element):
    try:
        #Get the existing element to replace
        element_to_replace = get_element_by_css_selector(page,selector)
        #Replace the existing element with the new element
        page.execute_script(f'arguments[0].replaceWith(arguments[1])', element_to_replace, new_html_element)
    except:
        pass
    
def send_enter_to_elem(page, css_selector):
    try:
        page.execute_script("""
        var element = document.querySelector('%s');
        var event = new KeyboardEvent('keydown', {'keyCode': 13, 'which': 13});
        element.dispatchEvent(event);""" % css_selector)
    except:
        pass

def open_new_winodw(page):
    try:
        # Switch to the last opened window using JavaScript
        page.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        page.switch_to.window(page.execute_script("return window.open('');"))
    except:
        pass


def switch_to_window(page, number:int):
    try:
        #Switch back to the previous window
        page.switch_to.window(page.window_handles[number])
    except:
        pass

def close_window(page):
    try:
        page.execute_script("window.close();")
    except:
        pass

def select_dropdown_item(page, css_selector, item_text):
    try:
        #Find the dropdown element by ID
        dropdown_element = get_element_by_css_selector(page,css_selector)

        #Use JavaScript to select the item by its visible text
        script = "var dropdown = arguments[0];" \
                    "var itemText = arguments[1];" \
                    "for (var i = 0; i < dropdown.options.length; ++i) {" \
                    "    if (dropdown.options[i].text === itemText) {" \
                    "        dropdown.selectedIndex = i;" \
                    "        dropdown.dispatchEvent(new Event('change', { bubbles: true }));" \
                    "        break;" \
                    "    }" \
                    "}"
        page.execute_script(script, dropdown_element, item_text)
        
    except Exception as e:
        log(f"An error occurred while selecting item '{item_text}' from dropdown '{css_selector}': {e}")

