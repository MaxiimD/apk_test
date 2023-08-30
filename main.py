from kivy.lang import Builder
from kivy.properties import ListProperty
from kivymd.app import MDApp
from kivymd.uix.list import OneLineAvatarIconListItem
from kivymd.uix.textfield import MDTextField
from firebase import firebase


# Builder.load_file('project.kv')


# class MyGridLayout(GridLayout):
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.cols = 2
#         self.search_bar = TextInput(multiline=False)
#         self.add_widget(self.search_bar)
#         self.search = Button().add_widget(Image())


class Search_Select_Option(OneLineAvatarIconListItem):
    def show_issue(self):
        pass


def get_issues_text_from_db():
    fb_app = firebase.FirebaseApplication(
        'https://communityconnect1234-default-rtdb.europe-west1.firebasedatabase.app/', None)
    billboard_db_data = fb_app.get('/Billboard', None)
    option_list = ""
    for dictionary in billboard_db_data:
        option_list += ','.join([msg for msg in dictionary.values()]) + ","
    option_list = option_list.split(',')
    return option_list


class SearchTextInput(MDTextField):

    def on_text(self, instance, value):
        self.get_issues_from_db_by_value(value)

    def get_issues_from_db_by_value(self, value):
        option_list = get_issues_text_from_db()
        app = MDApp.get_running_app()
        option_list = list(set(option_list + value[:value.rfind(' ')].split(' ')))
        val = value[value.rfind(' ') + 1:]
        if not val:
            return
        try:
            app.option_data = []
            for i in range(len(option_list)):
                word = [word for word in option_list if word.startswith(val)][0][len(val):]
                if not word:
                    return
                if self.text + word in option_list:
                    if self.text + word not in app.option_data:
                        popped_suggest = option_list.pop(option_list.index(str(self.text + word)))
                        app.option_data.append(popped_suggest)
                app.update_data(app.option_data)

        except IndexError:

            pass


class RVTestApp(MDApp):
    rv_data = ListProperty()

    def update_data(self, rv_data_list):
        self.rv_data = [{'text': item} for item in rv_data_list]
        print(self.rv_data, 'update')

    def build(self):
        self.rv_data = [{'text': item} for item in get_issues_text_from_db()]
        return Builder.load_file("project.kv")

    def erase(self):
        self.rv_data = []

    def search(self):
        pass


RVTestApp().run()
