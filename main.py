import os, json, string, uuid
os.system("pip install -qq selenium==4.4.3 webdriver-manager")
from dataclasses import dataclass
from random import choice, randint
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge import options
from names import names

os.system("cls || clear")
print("Microsoft Account Creator - senoe (DJStompZone Remix)")
print("DJ Stomp 2022 | No Rights Reserved | https://discord.gg/stompzone")
edge_options = options.Options()
edge_options.add_argument("--headless")
edge_options.add_experimental_option('excludeSwitches', ['enable-logging'])
accounts = []


cfg_signup_link = r"https://signup.live.com/signup?lcid=1033&wa=wsignin1.0&rpsnv=13&ct=1637807758&rver=7.0.6738.0&wp=MBI_SSL&wreply=https%3a%2f%2faccount.microsoft.com%2fauth%2fcomplete-signin%3fru%3dhttps%253A%252F%252Faccount.microsoft.com%252F%253Frefp%253Dsignedout-index%2526refd%253Dwww.google.com&lc=1033&id=292666&lw=1&fl=easi2&mkt=en-US&lic=1&uaid=4d50aa7e5a2c4d408a512ff3ff6a3f6a"


# Utility functions
def gen_email():
    return f"{choice(names)}{choice(['_','.',''])}{choice(names)}{str(randint(10000, 99999))[:randint(2,5)]}@outlook.com".lower()

def gen_pass(): 
    return "".join(choice(string.ascii_letters + string.punctuation  + string.digits) for x in range(randint(15, 24)))

def get_service():
    return Service(EdgeChromiumDriverManager().install())

def get_driver():
    return webdriver.Edge(service=get_service())


print("Launching webdriver...")
driver = get_driver()
wait = WebDriverWait(driver, 30)

@dataclass
class NewAccount():
    email: str = gen_email()
    password: str = gen_pass()
    country: str = "US"
    birth_year: int = randint(1970, 2001)
    birth_month: int = randint(1, 12)
    birthday: int = randint(1, 28) if birth_month in [2, 4, 6, 9, 11] else randint(1, 31)
    id: str = str(uuid.uuid4())
    hexid: str = uuid.UUID(id).hex

    def getJson(self):
        return {
            "email": self.email,
            "password": self.password,
            "country": self.country,
            "birth_month": self.birth_month,
            "birth_year": self.birth_year,
            "birthday": self.birthday,
            "id": self.id,
            "hexid": self.hexid
        }

def create():
    # Go to signup link
    driver.get(cfg_signup_link)
    account = NewAccount()
    
    print(f"Account creation started | {account.email}")
    

    # Enter email
    wait.until(EC.visibility_of_element_located((By.ID, "MemberName"))).send_keys(account.email)
    # Click Next
    wait.until(EC.visibility_of_element_located((By.ID, "iSignupAction"))).click()

    # Enter password
    wait.until(EC.visibility_of_element_located((By.ID, "PasswordInput"))).send_keys(account.password)
    # Uncheck promotion checkbox
    wait.until(EC.visibility_of_element_located((By.ID, "iOptinEmail"))).click()
    # Click Next
    wait.until(EC.visibility_of_element_located((By.ID, "iSignupAction"))).click()

    wait.until(EC.visibility_of_element_located((By.ID, "BirthDateCountryAccrualInputPane")))
    # Select country
    Select(driver.find_element(By.ID, "Country")).select_by_value(account.country)
    # Select birthday month
    Select(driver.find_element(By.ID, "BirthMonth")).select_by_value(str(account.birth_month))
    # Select birthday day
    Select(driver.find_element(By.ID, "BirthDay")).select_by_value(str(account.birthday))
    # Select birthday year
    driver.find_element(By.ID, "BirthYear").send_keys(str(account.birth_year))
    # Click Next
    wait.until(EC.visibility_of_element_located((By.ID, "iSignupAction"))).click()


    # Ask the user to manually complete the captcha
    wait.until(EC.visibility_of_element_located((By.ID, "enforcementFrame"))).click()
    # Todo: implement captcha solver for full automation
    print(f"Captcha completion required | {account.email=}")

    WebDriverWait(driver, 20000).until(EC.visibility_of_element_located((By.ID, "microsoft_container")))

    # Save credentials to file (old method for back-compatibility)
    with open("accounts.txt", "a") as f:
        f.write(f"{account.email}:{account.password}\n")

    # Save credentials to file (new method for interoperability and portability)
    # Todo: encrypt files for "proper" credential storage
    account_dir = os.getcwd()+os.path.sep+"accounts"
    if not os.path.isdir(account_dir):
        os.mkdir(account_dir)
    with open(f"{account_dir}{os.path.sep}{account.hexid}.json", "w") as fp:
        fp.write(json.dumps(account.getJson()))
        print(f"Account profile for {account.email} has been saved to {account_dir}{os.path.sep}{account.hexid}.json")
    
    print(f"Account created: {account.email}")

if __name__ == "__main__":
    create()
