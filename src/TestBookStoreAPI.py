import string

import requests
import re
import pytest
import datetime

"""content of test_BookStore.py"""


class TestBookStore:
    USERNAME = 'sli'
    PASSWORD = 'Asdf1234!'
    BASEURL = 'https://demoqa.com/'
    USERID = ''

    # Verify POST request to https://demoqa.com/Account/v1/Authorized'
    # Input : username, password
    # Expect: Response body is true. Status code is 200
    def test_account_v1_authorized(self, record_property):
        r = requests.post(TestBookStore.BASEURL + 'Account/v1/Authorized',
                          data={'userName': TestBookStore.USERNAME, 'password': TestBookStore.PASSWORD})
        assert r.status_code == 200
        record_property("Send correct credential to Account/v1/Authorized", "PASS")
        assert r.text == "true"
        record_property("Send correct credential to Account/v1/Authorized", "Response body is True")

    # Verify POST request to https://demoqa.com/Account/v1/GenerateToken
    # Input: username and password
    # Expect: Response return a token string.
    # Expect: expire date is 7 days after the current date
    # Expect: status = "Success" and result = "User authorized successfully"
    def test_account_v1_generate_token(self, record_property):
        r = requests.post(TestBookStore.BASEURL + 'Account/v1/GenerateToken',
                          data={'userName': TestBookStore.USERNAME, 'password': TestBookStore.PASSWORD})
        assert r.status_code == 200
        response = r.json()
        assert response["token"] != ""
        record_property("Token", "the token value is no empty string.")
        # Retrieve current data and time
        expireDate = datetime.date.today() + datetime.timedelta(days=7)
        # Convert expireDate to String with format yy--mm--dd. Compare the expireDate to the 7th date from current date.
        assert re.findall("^" + expireDate.strftime('%Y-%m-%d'), response["expires"])
        record_property("expireDate", "the expire Date is 7th date from current date.")
        assert response["status"] == "Success"
        record_property("status", "the status = Success")
        assert response["result"] == "User authorized successfully."
        record_property("result", "the result = User authorized successfully.")

    # Verify /Account/v1/User
    # Input: userName and password
    # Expect: userId, username and books
    def test_account_v1_user(self, record_property):
        NEWUSERID = string.ascii_letters
        r = requests.post(TestBookStore.BASEURL + "Account/v1/User",
                          data={'userName': NEWUSERID, 'password': TestBookStore.PASSWORD})
        assert r.status_code == 201
        response = r.json()
        TestBookStore.USERID = response['userID']
        print(TestBookStore.USERID)
        assert response['username'] == NEWUSERID

    # Verify retrieving Books list
    # Input: <none>
    # Expect: return 8 books information
    def test_bookstore_v1_books(self, record_property):
        r = requests.get(TestBookStore.BASEURL + 'BookStore/v1/Books')
        response =r.json()
        books = response["books"]

        # First book information
        assert books[0]['title'] == 'Git Pocket Guide'
        assert books[0]['subTitle'] == 'A Working Introduction'
        assert books[0]['author'] == 'Richard E. Silverman'
        assert re.findall("^2020-06-04", books[0]['publish_date'])
        assert books[0]['publisher'] == "O'Reilly Media"
        assert books[0]['pages'] == 234
        assert books[0]['description'] == 'This pocket guide is the perfect on-the-job companion to Git, ' \
                                          'the distributed version control system. It provides a compact, ' \
                                          'readable introduction to Git for new users, as well as a reference ' \
                                          'to common commands and procedures for those of you with Git exp'
        assert books[0]['website'] == 'http://chimera.labs.oreilly.com/books/1230000000561/index.html'

        #  Second book
        assert books[1]['title'] == 'Learning JavaScript Design Patterns'
        assert books[1]['subTitle'] == "A JavaScript and jQuery Developer's Guide"
        assert books[1]['author'] == 'Addy Osmani'
        assert re.findall("^2020-06-04", books[1]['publish_date'])
        assert books[1]['publisher'] == "O'Reilly Media"
        assert books[1]['pages'] == 254
        assert books[1]['description'] == "With Learning JavaScript Design Patterns, you'll learn how to " \
                                          "write beautiful, structured, and maintainable JavaScript by applying " \
                                          "classical and modern design patterns to the language. If you want to keep " \
                                          "your code efficient, more manageable, and up-to-da"
        assert books[1]['website'] == 'http://www.addyosmani.com/resources/essentialjsdesignpatterns/book/'

        # Third book
        assert books[2]['title'] == 'Designing Evolvable Web APIs with ASP.NET'
        assert books[2]['subTitle'] == "Harnessing the Power of the Web"
        assert books[2]['author'] == 'Glenn Block et al.'
        assert re.findall("^2020-06-04", books[2]['publish_date'])
        assert books[2]['publisher'] == "O'Reilly Media"
        assert books[2]['pages'] == 238
        assert books[2]['description'] == "Design and build Web APIs for a broad range of clients—including browsers" \
                                          " and mobile devices—that can adapt to change over time. This practical, " \
                                          "hands-on guide takes you through the theory and tools you need to build " \
                                          "evolvable HTTP services with Microsoft"
        assert books[2]['website'] == 'http://chimera.labs.oreilly.com/books/1234000001708/index.html'

        # Forth Book
        assert books[3]['title'] == 'Speaking JavaScript'
        assert books[3]['subTitle'] == "An In-Depth Guide for Programmers"
        assert books[3]['author'] == 'Axel Rauschmayer'
        assert re.findall("^2014-02-01", books[3]['publish_date'])
        assert books[3]['publisher'] == "O'Reilly Media"
        assert books[3]['pages'] == 460
        assert books[3]['description'] == "Like it or not, JavaScript is everywhere these days-from browser to" \
                                          " server to mobile-and now you, too, need to learn the language or dive" \
                                          " deeper than you have. This concise book guides you into and through" \
                                          " JavaScript, written by a veteran programmer who o"
        assert books[3]['website'] == 'http://speakingjs.com/'

        # Fifth Book
        assert books[4]['title'] == "You Don't Know JS"
        assert books[4]['subTitle'] == "ES6 & Beyond"
        assert books[4]['author'] == 'Kyle Simpson'
        assert re.findall("^2015-12-27", books[4]['publish_date'])
        assert books[4]['publisher'] == "O'Reilly Media"
        assert books[4]['pages'] == 278
        assert books[4]['description'] == "No matter how much experience you have with JavaScript, odds are you don’t " \
                                          "fully understand the language. As part of the \\\"You Don’t Know JS\\\" series, " \
                                          "this compact guide focuses on new features available in ECMAScript 6 (ES6), the latest version of the st"
        assert books[4]['website'] == 'https://github.com/getify/You-Dont-Know-JS/tree/master/es6%20&%20beyond'

        # Sixth Book
        assert books[5]['title'] == "Programming JavaScript Applications"
        assert books[5]['subTitle'] == "Robust Web Architecture with Node, HTML5, and Modern JS Libraries"
        assert books[5]['author'] == 'Eric Elliott'
        assert re.findall("^2014-07-01", books[5]['publish_date'])
        assert books[5]['publisher'] == "O'Reilly Media"
        assert books[5]['pages'] == 254
        assert books[5]['description'] == "Take advantage of JavaScript's power to build robust web-scale " \
                                          "or enterprise applications that are easy to extend and maintain. " \
                                          "By applying the design patterns outlined in this practical book, " \
                                          "experienced JavaScript developers will learn how to write flex"
        assert books[5]['website'] == 'http://chimera.labs.oreilly.com/books/1234000000262/index.html'

        # Seventh Book
        assert books[6]['title'] == "Eloquent JavaScript, Second Edition"
        assert books[6]['subTitle'] == "A Modern Introduction to Programming"
        assert books[6]['author'] == 'Marijn Haverbeke'
        assert re.findall("^2014-12-14", books[6]['publish_date'])
        assert books[6]['publisher'] == "No Starch Press"
        assert books[6]['pages'] == 472
        assert books[6]['description'] == "JavaScript lies at the heart of almost every modern web application, " \
                                          "from social apps to the newest browser-based games. Though simple for " \
                                          "beginners to pick up and play with, JavaScript is a flexible, complex " \
                                          "language that you can use to build full-scale "
        assert books[6]['website'] == 'http://eloquentjavascript.net/'

        # Eighth Book
        assert books[7]['title'] == "Understanding ECMAScript 6"
        assert books[7]['subTitle'] == "The Definitive Guide for JavaScript Developers"
        assert books[7]['author'] == 'Nicholas C. Zakas'
        assert re.findall("^2016-09-03", books[7]['publish_date'])
        assert books[7]['publisher'] == "No Starch Press"
        assert books[7]['pages'] == 352
        assert books[7]['description'] == "ECMAScript 6 represents the biggest update to the core of JavaScript " \
                                          "in the history of the language. In Understanding ECMAScript 6, " \
                                          "expert developer Nicholas C. Zakas provides a complete guide to the" \
                                          " object types, syntax, and other exciting changes that E"
        assert books[7]['website'] == 'https://leanpub.com/understandinges6/read'