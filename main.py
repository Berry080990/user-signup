import webapp2
import re


page_layout = """
<!DOCTYPE html>
<html>
    <head>
        <style>
            .error {
            color : red;
            }
        </style>
    </head>

    <body>
        <h1>Signup</h1>
        <form method="post">
            <div>
                <label for="username">Username</label>
                <input name="username" type="text" value=%(username)s>
                <span class="error">%(errora)s</span>
            </div>
            <div>
                <label for="password">Password</label>
                <input name="password" type="password" value="">
                <span class="error">%(errorb)s</span>
            </div>
            <div>
                <label for="verify">Verify Password</label>
                <input name="verify" type="password" value="">
                <span class="error">%(errorc)s</span>
            </div>
            <div>
                <label for="email">Email (optional)</label>
                <input name="email type="text" value=%(email)s>
                <span class="error">%(errord)s</span>
            </div>
        <input type="submit">
    </form>
    </body>
</html>
"""
welcome_user = ""

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

class MainHandler(webapp2.RequestHandler):
    def write_form(self, username = "", email = "", errora = "", errorb = "", errorc = "", errord = ""):
        self.response.write(page_layout % {"username" : username, "email" : email, "errora" : errora, "errorb" : errorb, "errorc" : errorc, "errord" : errord})

    def get(self):
        self.write_form()


    def post(self):
        user_username = self.request.get("username")
        user_password = self.request.get("password")
        user_verify = self.request.get("verify")
        user_email = self.request.get("email")

        username = user_username
        password = user_password
        verify = user_verify
        email = user_email

        if not valid_username(username):
            self.write_form(user_username, user_email, "That is not a valid username.")

        elif not valid_password(password):
            self.write_form(user_username, user_email, "", "That is not a valid password.")

        elif password != verify:
            self.write_form(user_username, user_email, "", "", "The passwords do not match.")

        elif not valid_email(email):
            self.write_form(user_username, user_email, "", "", "", "That is not a valid email.")

        else:
            welcome_user = (username)
            return self.redirect('/welcome')

class Welcome(webapp2.RequestHandler):
    def get(self):
        self.response.out.write("Welcome, " + welcome_user + "!")


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/welcome', Welcome)
], debug=True)
