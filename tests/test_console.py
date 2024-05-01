#!/usr/bin/python3
"""test for console"""
import unittest
from unittest.mock import patch
from io import StringIO
import pep8
import os
import json
import console
import tests
import MySQLdb
from console import HBNBCommand
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.engine.file_storage import FileStorage
from models import storage
from models.engine.db_storage import DBStorage
from sqlalchemy import (create_engine)
from sqlalchemy.orm import sessionmaker, relationship, backref, scoped_session

try:
    My_user = os.environ['HBNB_MYSQL_USER']
    My_pw = os.environ['HBNB_MYSQL_PWD']
    My_host = os.environ['HBNB_MYSQL_HOST']
    My_db = os.environ['HBNB_MYSQL_DB']
    My_storage = os.environ['HBNB_TYPE_STORAGE']
except:
    My_user = None
    My_pw = None
    My_host = None
    My_db = None
    My_storage = None


class TestConsole(unittest.TestCase):
    """this will test the console"""

    @classmethod
    def setUpClass(cls):
        """setup for the test"""
        cls.consol = HBNBCommand()

    @classmethod
    def teardown(cls):
        """at the end of the test this will tear it down"""
        del cls.consol

    def tearDown(self):
        """Remove temporary file (file.json) created as a result"""
        if My_storage != 'db':
            try:
                os.remove("file.json")
            except Exception:
                pass

    def test_pep8_console(self):
        """Pep8 console.py"""
        style = pep8.StyleGuide(quiet=True)
        p = style.check_files(["console.py"])
        self.assertEqual(p.total_errors, 0, 'fix Pep8')

    def test_docstrings_in_console(self):
        """checking for docstrings"""
        self.assertIsNotNone(console.__doc__)
        self.assertIsNotNone(HBNBCommand.emptyline.__doc__)
        self.assertIsNotNone(HBNBCommand.do_quit.__doc__)
        self.assertIsNotNone(HBNBCommand.do_EOF.__doc__)
        self.assertIsNotNone(HBNBCommand.do_create.__doc__)
        self.assertIsNotNone(HBNBCommand.do_show.__doc__)
        self.assertIsNotNone(HBNBCommand.do_destroy.__doc__)
        self.assertIsNotNone(HBNBCommand.do_all.__doc__)
        self.assertIsNotNone(HBNBCommand.do_update.__doc__)
        self.assertIsNotNone(HBNBCommand.count.__doc__)
        self.assertIsNotNone(HBNBCommand.strip_clean.__doc__)
        self.assertIsNotNone(HBNBCommand.default.__doc__)

    def test_emptyline(self):
        """Test empty line input"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("\n")
            self.assertEqual('', f.getvalue())

    def test_quit(self):
        """test quit command inpout"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("quit")
            self.assertEqual('', f.getvalue())

    def test_create_0(self):
        """Test create command inpout for invalid input"""
        if My_storage == 'db':
            pass
        else:
            with patch('sys.stdout', new=StringIO()) as f:
                self.consol.onecmd("create")
                self.assertEqual(
                    "** class name missing **\n", f.getvalue())
            with patch('sys.stdout', new=StringIO()) as f:
                self.consol.onecmd("create asdfsfsd")
                self.assertEqual(
                    "** class doesn't exist **\n", f.getvalue())
            with patch('sys.stdout', new=StringIO()) as f:
                self.consol.onecmd("create State a")
                self.assertEqual("\n", f.getvalue())
            with patch('sys.stdout', new=StringIO()) as f:
                self.consol.onecmd("create State name")
                self.assertEqual("\n", f.getvalue())
            with patch('sys.stdout', new=StringIO()) as f:
                self.consol.onecmd("create State b=")
                self.assertEqual("\n", f.getvalue())

    def test_create_1(self):
        """Test create command inpout for User"""
        if My_storage == 'db':
            db = MySQLdb.connect(host=My_host, user=My_user,
                                 passwd=My_pw, db=My_db)
            cur = db.cursor()
            with patch('sys.stdout', new=StringIO()) as f:
                self.consol.onecmd('create User User email="gui@hbtn.io" \
                password="guipwd" first_name="Guillaume" last_name="Snow"')
                string1 = f.getvalue()
            with patch('sys.stdout', new=StringIO()) as f:
                self.consol.onecmd("all User")
                self.assertEqual("[[User]", f.getvalue()[:7])
            cur.execute("SELECT * FROM users")
            rows = cur.fetchall()
            for row in rows:
                if row[0] == string1[:-1]:
                    self.assertEqual("gui@hbtn.io", row.email)
                    self.assertEqual("guipwd", row.password)
                    self.assertEqual("Guillaume", row.first_name)
                    self.assertEqual("Snow", row.last_name)
            try:
                cur.execute("DELETE TABLE users")
            except:
                pass

        else:
            with patch('sys.stdout', new=StringIO()) as f:
                self.consol.onecmd("create User")
                string = f.getvalue()
                key = "User." + string[:-1]
                all_objs = storage.all()
                self.assertTrue(key in list(all_objs.keys()))
                filename = FileStorage._FileStorage__file_path
                lis = []
                if os.path.isfile(filename):
                    with open(filename, 'r') as f:
                        dic = json.loads(f.read())
                    for v in dic.values():
                        lis += [v['id']]
                self.assertTrue(string[:-1] in lis)
            with patch('sys.stdout', new=StringIO()) as f:
                self.consol.onecmd("all User")
                self.assertEqual(
                    "[[User]", f.getvalue()[:7])
            with patch('sys.stdout', new=StringIO()) as f:
                self.consol.onecmd("create State")
            with patch('sys.stdout', new=StringIO()) as f:
                self.consol.onecmd("all State")
                self.assertEqual(
                    "[[State]", f.getvalue()[:8])

    def test_create_2(self):
        """Test create command inpout for City"""
        if My_storage == 'db':
            db = MySQLdb.connect(host=My_host, user=My_user,
                                 passwd=My_pw, db=My_db)
            cur = db.cursor()
            with patch('sys.stdout', new=StringIO()) as f:
                self.consol.onecmd("create State name='California'")
                string1 = f.getvalue()
                self.consol.onecmd("create City name='San_Francisco' \
                state_id={}".format(string1))
                string2 = f.getvalue()[len(string1):-1]
                cur.execute("SELECT * FROM states")
                states = cur.fetchall()
                for state in states:
                    if state[0] == string1[:-1]:
                        self.assertEqual(state[0], string1[:-1])
                cur.execute("SELECT * FROM cities")
                cities = cur.fetchall()
                for city in cities:
                    if city[0] == string1[:-1]:
                        self.assertEqual(city[0], string1[:-1])
            with patch('sys.stdout', new=StringIO()) as f:
                self.consol.onecmd("all State")
                self.assertEqual(
                    "[[State]", f.getvalue()[:8])
            with patch('sys.stdout', new=StringIO()) as f:
                self.consol.onecmd("all City")
                self.assertEqual(
                    "[[City]", f.getvalue()[:7])
            try:
                cur.execute("DROP TABLE cities")
            except:
                pass
            try:
                cur.execute("DROP TABLE states")
            except:
                pass
            cur.close()
            db.close()
        else:
            with patch('sys.stdout', new=StringIO()) as f:
                self.consol.onecmd("create City")
                string = f.getvalue()
                key = "City." + string[:-1]
                all_objs = storage.all()
                self.assertTrue(key in list(all_objs.keys()))
                filename = FileStorage._FileStorage__file_path
                lis = []
                if os.path.isfile(filename):
                    with open(filename, 'r') as f:
                        dic = json.loads(f.read())
                    for v in dic.values():
                        lis += [v['id']]
                self.assertTrue(string[:-1] in lis)
            with patch('sys.stdout', new=StringIO()) as f:
                self.consol.onecmd("all City")
                self.assertEqual(
                    "[[City]", f.getvalue()[:7])

    def test_create_3(self):
        """Test create command inpout for City"""
        if My_storage == 'db':
            pass
        else:
            with patch('sys.stdout', new=StringIO()) as f:
                self.consol.onecmd("create State")
                string = f.getvalue()
                key = "State." + string[:-1]
                all_objs = storage.all()
                self.assertTrue(key in list(all_objs.keys()))
                filename = FileStorage._FileStorage__file_path
                lis = []
                if os.path.isfile(filename):
                    with open(filename, 'r') as f:
                        dic = json.loads(f.read())
                    for v in dic.values():
                        lis += [v['id']]
                self.assertTrue(string[:-1] in lis)
            with patch('sys.stdout', new=StringIO()) as f:
                self.consol.onecmd("all State")
                self.assertEqual(
                    "[[State]", f.getvalue()[:8])

    def test_create_4(self):
        """Test create command when input is name=A=B,
            value shoule be A=B"""
        if My_storage == 'db':
            db = MySQLdb.connect(host=My_host, user=My_user,
                                 passwd=My_pw, db=My_db)
            cur = db.cursor()
            with patch('sys.stdout', new=StringIO()) as f:
                self.consol.onecmd("create State name='A=B'")
                string1 = f.getvalue()
                cur.execute("SELECT * FROM states")
                states = cur.fetchall()
                for state in states:
                    if state[0] == string1[:-1]:
                        self.assertEqual(state[0], string1[:-1])
                try:
                    cur.execute("DROP TABLE cities")
                except:
                    pass
                try:
                    cur.execute("DROP TABLE states")
                except:
                    pass
            cur.close()
            db.close()
        else:
            with patch('sys.stdout', new=StringIO()) as f:
                self.consol.onecmd("create State name=A=B")
                string = f.getvalue()
                key = "State." + string[:-1]
                all_objs = storage.all()
                self.assertEqual("A=B", all_objs[key].__dict__['name'])

    def test_create_4_1(self):
        """Test create command when input is name='North_Carolina',
            value shoule be North_Carolina"""
        if My_storage == 'db':
            pass
        else:
            with patch('sys.stdout', new=StringIO()) as f:
                self.consol.onecmd('create State name="North_Carolina"')
                string = f.getvalue()
                key = "State." + string[:-1]
                all_objs = storage.all()
                self.assertEqual("North Carolina",
                                 all_objs[key].__dict__['name'])

    def test_create_5(self):
        """Test create command inpout for BaseModel"""
        if My_storage == 'db':
            pass
        else:
            with patch('sys.stdout', new=StringIO()) as f:
                self.consol.onecmd("create BaseModel")
                string = f.getvalue()
                key = "BaseModel." + string[:-1]
                all_objs = storage.all()
                self.assertTrue(key in list(all_objs.keys()))
                filename = FileStorage._FileStorage__file_path
                lis = []
                if os.path.isfile(filename):
                    with open(filename, 'r') as f:
                        dic = json.loads(f.read())
                    for v in dic.values():
                        lis += [v['id']]
                self.assertTrue(string[:-1] in lis)
            with patch('sys.stdout', new=StringIO()) as f:
                self.consol.onecmd("all BaseModel")
                self.assertEqual(
                    "[[BaseModel]", f.getvalue()[:12])

    def test_create_6(self):
        """Test create command inpout for Amenity"""
        if My_storage == 'db':
            pass
        else:
            with patch('sys.stdout', new=StringIO()) as f:
                self.consol.onecmd("create Amenity")
                string = f.getvalue()
                key = "Amenity." + string[:-1]
                all_objs = storage.all()
                self.assertTrue(key in list(all_objs.keys()))
                filename = FileStorage._FileStorage__file_path
                lis = []
                if os.path.isfile(filename):
                    with open(filename, 'r') as f:
                        dic = json.loads(f.read())
                    for v in dic.values():
                        lis += [v['id']]
                self.assertTrue(string[:-1] in lis)
            with patch('sys.stdout', new=StringIO()) as f:
                self.consol.onecmd("all Amenity")
                self.assertEqual(
                    "[[Amenity]", f.getvalue()[:10])

    def test_create_7(self):
        """Test create command inpout for Place"""
        if My_storage == 'db':
            db = MySQLdb.connect(host=My_host, user=My_user,
                                 passwd=My_pw, db=My_db)
            cur = db.cursor()
            with patch('sys.stdout', new=StringIO()) as f:
                self.consol.onecmd('create State name="Utah"')
                string0 = f.getvalue()
            with patch('sys.stdout', new=StringIO()) as f:
                self.consol.onecmd('create City name="Anaheim" state_id={}'.
                                   format(string0[:-1]))
                string1 = f.getvalue()
            with patch('sys.stdout', new=StringIO()) as f:
                self.consol.onecmd('create User User email="gui@hbtn.io" \
                password="guipwd" first_name="Guillaume" last_name="Snow"')
                string2 = f.getvalue()
            with patch('sys.stdout', new=StringIO()) as f:
                self.consol.onecmd('create Place city_id={} user_id={} \
                name="Lovely_place" number_rooms=3 number_bathrooms=1 \
                max_guest=6 price_by_night=120 latitude=37.773972 \
                longitude=-122.431297'.format(string1, string2))
                string3 = f.getvalue()
                cur.execute("SELECT * FROM places")
                places = cur.fetchall()
                for place in places:
                    if place[0] == string3[:-1]:
                        self.assertEqual(place[0].number_rooms, 3)
                        self.assertEqual(place[0].number_bathrooms, 1)
                        self.assertEqual(round(place[0].latitude, 6),
                                         round(37.773972, 6))
                        self.assertEqual(round(place[0].longitude, 6),
                                         round(-122.431297, 6))
            with patch('sys.stdout', new=StringIO()) as f:
                self.consol.onecmd('all Place')
                self.assertEqual(
                    "[[Place]", f.getvalue()[:8])
            with patch('sys.stdout', new=StringIO()) as f:
                self.consol.onecmd('create Review place_id={} user_id={} \
                text="Amazing_place,_huge_kitchen"'.format(string3[:-1],
                                                           string0[:-1]))
                string4 = f.getvalue()
                cur.execute("SELECT * FROM reviews")
                reviews = cur.fetchall()
                for review in reviews:
                    if review[0] == string4[:-1]:
                        self.assertEqual(review[0].text,
                                         "Amazing_place,_huge_kitchen")
                        break
            try:
                cur.execute("DROP TABLE places")
            except:
                pass
            try:
                cur.execute("DROP TABLE users")
            except:
                pass
            try:
                cur.execute("DROP TABLE cities")
            except:
                pass
            try:
                cur.execute("DROP TABLE states")
            except:
                pass
            cur.close()
            db.close()
        else:
            with patch('sys.stdout', new=StringIO()) as f:
                self.consol.onecmd("""create Place""")
                string = f.getvalue()
                key = "Place." + string[:-1]
                all_objs = storage.all()
                self.assertTrue(key in list(all_objs.keys()))
                filename = FileStorage._FileStorage__file_path
                lis = []
                if os.path.isfile(filename):
                    with open(filename, 'r') as f:
                        dic = json.loads(f.read())
                    for v in dic.values():
                        lis += [v['id']]
                self.assertTrue(string[:-1] in lis)
            with patch('sys.stdout', new=StringIO()) as f:
                self.consol.onecmd("all Place")
                self.assertEqual(
                    "[[Place]", f.getvalue()[:8])

    def test_create_7_1(self):
        """Test create command when input is <value> by not a string type,
            value shoule be formated accordingly"""
        if My_storage == 'db':
            pass
        else:
            with patch('sys.stdout', new=StringIO()) as f:
                self.consol.onecmd('create Place city_id="0001" \
                user_id="0001" name="My_little_house" number_rooms=4 \
                number_bathrooms=2 max_guest=10 price_by_night=300 \
                latitude=37.773972 longitude=-122.431297')
                string = f.getvalue()
                key = "Place." + string[:-1]
                all_objs = storage.all()
                self.assertTrue(key in list(all_objs.keys()))
                for k, v in all_objs[key].__dict__.items():
                    if k == 'name':
                        self.assertEqual("My little house", v)
                    if k == 'price_by_night':
                        self.assertEqual(300, v)
                    if k == 'number_rooms':
                        self.assertEqual(4, v)
                    if k == 'max_guest':
                        self.assertEqual(10, v)
                    if k == 'number_bathrooms':
                        self.assertEqual(2, v)
                    if k == 'latitude':
                        self.assertEqual(round(37.773972, 6), round(v, 6))
                    if k == 'longitude':
                        self.assertEqual(round(-122.431297, 6), round(v, 6))

    def test_create_8(self):
        """Test create command inpout for Review"""
        if My_storage == 'db':
            pass
        else:
            with patch('sys.stdout', new=StringIO()) as f:
                self.consol.onecmd("create Review")
                string = f.getvalue()
                key = "Review." + string[:-1]
                all_objs = storage.all()
                self.assertTrue(key in list(all_objs.keys()))
                filename = FileStorage._FileStorage__file_path
                lis = []
                if os.path.isfile(filename):
                    with open(filename, 'r') as f:
                        dic = json.loads(f.read())
                    for v in dic.values():
                        lis += [v['id']]
                self.assertTrue(string[:-1] in lis)
            with patch('sys.stdout', new=StringIO()) as f:
                self.consol.onecmd("all Review")
                self.assertEqual(
                    "[[Review]", f.getvalue()[:9])

    def test_show(self):
        """Test show command inpout"""
        if My_storage == 'db':
            pass
        else:
            with patch('sys.stdout', new=StringIO()) as f:
                self.consol.onecmd("show")
                self.assertEqual(
                    "** class name missing **\n", f.getvalue())
            with patch('sys.stdout', new=StringIO()) as f:
                self.consol.onecmd("show asdfsdrfs")
                self.assertEqual(
                    "** class doesn't exist **\n", f.getvalue())
            with patch('sys.stdout', new=StringIO()) as f:
                self.consol.onecmd("show BaseModel")
                self.assertEqual(
                    "** instance id missing **\n", f.getvalue())
            with patch('sys.stdout', new=StringIO()) as f:
                self.consol.onecmd("show BaseModel abcd-123")
                self.assertEqual(
                    "** no instance found **\n", f.getvalue())

    def test_destroy(self):
        """Test destroy command inpout"""
        if My_storage == 'db':
            pass
        else:
            with patch('sys.stdout', new=StringIO()) as f:
                self.consol.onecmd("destroy")
                self.assertEqual(
                    "** class name missing **\n", f.getvalue())
            with patch('sys.stdout', new=StringIO()) as f:
                self.consol.onecmd("destroy Galaxy")
                self.assertEqual(
                    "** class doesn't exist **\n", f.getvalue())
            with patch('sys.stdout', new=StringIO()) as f:
                self.consol.onecmd("destroy User")
                self.assertEqual(
                    "** instance id missing **\n", f.getvalue())
            with patch('sys.stdout', new=StringIO()) as f:
                self.consol.onecmd("destroy BaseModel 12345")
                self.assertEqual(
                    "** no instance found **\n", f.getvalue())

    def test_all(self):
        """Test all command inpout"""
        if My_storage == 'db':
            pass
        else:
            with patch('sys.stdout', new=StringIO()) as f:
                self.consol.onecmd("all asdfsdfsd")
                self.assertEqual("** class doesn't exist **\n", f.getvalue())
            with patch('sys.stdout', new=StringIO()) as f:
                self.consol.onecmd("all State")
                self.assertEqual("[]\n", f.getvalue())

    def test_update(self):
        """Test update command inpout"""
        if My_storage == 'db':
            pass
        else:
            with patch('sys.stdout', new=StringIO()) as f:
                self.consol.onecmd("update")
                self.assertEqual(
                    "** class name missing **\n", f.getvalue())
            with patch('sys.stdout', new=StringIO()) as f:
                self.consol.onecmd("update sldkfjsl")
                self.assertEqual(
                    "** class doesn't exist **\n", f.getvalue())
            with patch('sys.stdout', new=StringIO()) as f:
                self.consol.onecmd("update User")
                self.assertEqual(
                    "** instance id missing **\n", f.getvalue())
            with patch('sys.stdout', new=StringIO()) as f:
                self.consol.onecmd("update User 12345")
                self.assertEqual(
                    "** no instance found **\n", f.getvalue())
            with patch('sys.stdout', new=StringIO()) as f:
                self.consol.onecmd("all User")
                obj = f.getvalue()
            my_id = obj[obj.find('(')+1:obj.find(')')]
            with patch('sys.stdout', new=StringIO()) as f:
                self.consol.onecmd("update User " + my_id)
                self.assertEqual(
                    "** attribute name missing **\n", f.getvalue())
            with patch('sys.stdout', new=StringIO()) as f:
                self.consol.onecmd("update User " + my_id + " Name")
                self.assertEqual(
                    "** value missing **\n", f.getvalue())

    def test_z_all(self):
        """Test alternate all command inpout"""
        if My_storage == 'db':
            pass
        else:
            with patch('sys.stdout', new=StringIO()) as f:
                self.consol.onecmd("asdfsdfsd.all()")
                self.assertEqual(
                    "** class doesn't exist **\n", f.getvalue())
            # with patch('sys.stdout', new=StringIO()) as f:
            #     self.consol.onecmd("State.all()")
            #     self.assertEqual("[]\n", f.getvalue())

    def test_z_count(self):
        """Test count command inpout"""
        if My_storage == 'db':
            pass
        else:
            with patch('sys.stdout', new=StringIO()) as f:
                self.consol.onecmd("asdfsdfsd.count()")
                self.assertEqual(
                    "** class doesn't exist **\n", f.getvalue())
            # with patch('sys.stdout', new=StringIO()) as f:
            #     self.consol.onecmd("State.count()")
            #     self.assertEqual("0\n", f.getvalue())

    def test_z_show(self):
        """Test alternate show command inpout"""
        if My_storage == 'db':
            pass
        else:
            with patch('sys.stdout', new=StringIO()) as f:
                self.consol.onecmd("safdsa.show()")
                self.assertEqual(
                    "** class doesn't exist **\n", f.getvalue())
            with patch('sys.stdout', new=StringIO()) as f:
                self.consol.onecmd("BaseModel.show(abcd-123)")
                self.assertEqual(
                    "** no instance found **\n", f.getvalue())

    def test_destroy(self):
        """Test alternate destroy command inpout"""
        if My_storage == 'db':
            pass
        else:
            with patch('sys.stdout', new=StringIO()) as f:
                self.consol.onecmd("Galaxy.destroy()")
                self.assertEqual(
                    "** class doesn't exist **\n", f.getvalue())
            with patch('sys.stdout', new=StringIO()) as f:
                self.consol.onecmd("User.destroy(12345)")
                self.assertEqual(
                    "** no instance found **\n", f.getvalue())

    def test_update(self):
        """Test alternate destroy command inpout"""
        if My_storage == 'db':
            pass
        else:
            with patch('sys.stdout', new=StringIO()) as f:
                self.consol.onecmd("sldkfjsl.update()")
                self.assertEqual(
                    "** class doesn't exist **\n", f.getvalue())
            with patch('sys.stdout', new=StringIO()) as f:
                self.consol.onecmd("User.update(12345)")
                self.assertEqual(
                    "** no instance found **\n", f.getvalue())
            with patch('sys.stdout', new=StringIO()) as f:
                self.consol.onecmd("all User")
                obj = f.getvalue()
            my_id = obj[obj.find('(')+1:obj.find(')')]
            with patch('sys.stdout', new=StringIO()) as f:
                self.consol.onecmd("User.update(" + my_id + ")")
                self.assertEqual(
                    "** attribute name missing **\n", f.getvalue())
            with patch('sys.stdout', new=StringIO()) as f:
                self.consol.onecmd("User.update(" + my_id + ", name)")
                self.assertEqual(
                    "** value missing **\n", f.getvalue())

if __name__ == "__main__":
    unittest.main()
