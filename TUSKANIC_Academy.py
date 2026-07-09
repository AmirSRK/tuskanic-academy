from kivy.lang import Builder
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.properties import StringProperty, BooleanProperty, NumericProperty, ListProperty
from kivy.uix.widget import Widget
from kivy.uix.behaviors import ButtonBehavior
from kivy.graphics import Color, RoundedRectangle, Ellipse
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import MDList, OneLineIconListItem, IconLeftWidget
from kivymd.uix.selectioncontrol import MDSwitch


# ==================================================
# CUSTOM DARK/LIGHT MODE TOGGLE
# ==================================================
# A small pill-shaped switch with a smoothly animated white knob and
# a track that fades between light grey and the app's purple accent.
# Replaces the stock MDSwitch, which looks the same as every other
# switch in the app and doesn't tie visually into the "theme" idea.
class ThemeSwitch(ButtonBehavior, Widget):
    active = BooleanProperty(False)
    thumb_x = NumericProperty(0)
    track_color = ListProperty([0.89, 0.89, 0.91, 1])

    LIGHT_TRACK = [0.89, 0.89, 0.91, 1]
    DARK_TRACK = [0.36, 0.18, 1.0, 1]  # matches app accent #5B2EFF

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (dp(56), dp(30))
        self.bind(
            pos=self._redraw,
            size=self._redraw,
            thumb_x=self._redraw,
            track_color=self._redraw,
            active=self._on_active_changed,
        )
        # set the visual state once layout has settled, same reasoning
        # as the old MDSwitch sync: doing it immediately would use a
        # width of 0 and leave the knob in the wrong spot.
        Clock.schedule_once(lambda dt: self._on_active_changed(self, self.active, animate=False), 0)

    def _on_active_changed(self, instance, value, animate=True):
        target_x = self.width - self.height if value else 0
        target_color = self.DARK_TRACK if value else self.LIGHT_TRACK
        if animate:
            anim = (Animation(thumb_x=target_x, duration=0.18, t="out_quad")
                     & Animation(track_color=target_color, duration=0.18, t="out_quad"))
            anim.start(self)
        else:
            self.thumb_x = target_x
            self.track_color = target_color

    def on_release(self):
        self.active = not self.active

    def _redraw(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(rgba=self.track_color)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[self.height / 2])
            Color(rgba=(1, 1, 1, 1))
            d = self.height - dp(4)
            Ellipse(pos=(self.x + self.thumb_x + dp(2), self.y + dp(2)), size=(d, d))

KV = '''
#:import Window kivy.core.window.Window

MDScreenManager:
    id: screen_manager
    MainScreen:
    DashboardScreen:
    CoursesScreen:
    TeachersScreen:
    CertificatesScreen:
    ScheduleScreen:
    SupportScreen:
    LoginScreen:
    SignupScreen:
    AccountScreen:
    ChatNotificationsScreen:
    LanguageScreen:
    ChatSettingsScreen:
    PrivacyScreen:


# ==================================================
# GLOBAL SCREEN BACKGROUND (reacts to Dark/Light mode)
# ==================================================
# Every screen in the app (MainScreen, DashboardScreen, etc.) inherits
# from MDScreen, so this single rule makes ALL of them follow the
# current theme automatically. Without this, toggling the switch only
# changes app.theme_cls.theme_style internally but nothing visible
# updates, since none of the screens were bound to a theme color.
<MDScreen>:
    md_bg_color: app.theme_cls.bg_normal


# ==================================================
# BOTTOM BAR TEMPLATE
# ==================================================

<BottomBar@MDBoxLayout>:
    size_hint_y: None
    height: "72dp"
    md_bg_color: app.theme_cls.bg_normal
    padding: "5dp", "8dp"
    spacing: "0dp"

    canvas.before:
        Color:
            rgba: 0.85, 0.85, 0.85, 1
        Rectangle:
            pos: self.pos[0], self.pos[1] + self.height - 1
            size: self.width, 1

    # HOME
    MDBoxLayout:
        orientation: "vertical"
        spacing: "2dp"
        on_touch_down:
            if self.collide_point(*args[1].pos): app.go_to("main")

        MDIconButton:
            icon: "home"
            pos_hint: {"center_x": .5}
            size_hint: None, None
            size: "40dp", "40dp"
            theme_text_color: "Custom"
            text_color: "#5B2EFF" if app.current_screen == "main" else "#888888"
            on_release: app.go_to("main")

        MDLabel:
            text: "Home"
            halign: "center"
            font_size: "11sp"
            size_hint_y: None
            height: "16dp"
            theme_text_color: "Custom"
            text_color: "#5B2EFF" if app.current_screen == "main" else "#888888"

    # COURSES
    MDBoxLayout:
        orientation: "vertical"
        spacing: "2dp"

        MDIconButton:
            icon: "book-open-page-variant"
            pos_hint: {"center_x": .5}
            size_hint: None, None
            size: "40dp", "40dp"
            theme_text_color: "Custom"
            text_color: "#5B2EFF" if app.current_screen == "courses" else "#888888"
            on_release: app.go_to("courses")

        MDLabel:
            text: "Courses"
            halign: "center"
            font_size: "11sp"
            size_hint_y: None
            height: "16dp"
            theme_text_color: "Custom"
            text_color: "#5B2EFF" if app.current_screen == "courses" else "#888888"

    # MESSAGES
    MDBoxLayout:
        orientation: "vertical"
        spacing: "2dp"

        MDIconButton:
            icon: "message-outline"
            pos_hint: {"center_x": .5}
            size_hint: None, None
            size: "40dp", "40dp"
            theme_text_color: "Custom"
            text_color: "#5B2EFF" if app.current_screen == "support" else "#888888"
            on_release: app.go_to("support")

        MDLabel:
            text: "Messages"
            halign: "center"
            font_size: "11sp"
            size_hint_y: None
            height: "16dp"
            theme_text_color: "Custom"
            text_color: "#5B2EFF" if app.current_screen == "support" else "#888888"

    # NOTIFICATIONS
    MDBoxLayout:
        orientation: "vertical"
        spacing: "2dp"

        MDIconButton:
            icon: "bell-outline"
            pos_hint: {"center_x": .5}
            size_hint: None, None
            size: "40dp", "40dp"
            theme_text_color: "Custom"
            text_color: "#5B2EFF" if app.current_screen == "dashboard" else "#888888"
            on_release: app.go_to("dashboard")

        MDLabel:
            text: "Notifications"
            halign: "center"
            font_size: "11sp"
            size_hint_y: None
            height: "16dp"
            theme_text_color: "Custom"
            text_color: "#5B2EFF" if app.current_screen == "dashboard" else "#888888"

    # MORE
    MDBoxLayout:
        orientation: "vertical"
        spacing: "2dp"

        MDIconButton:
            icon: "dots-grid"
            pos_hint: {"center_x": .5}
            size_hint: None, None
            size: "40dp", "40dp"
            theme_text_color: "Custom"
            text_color: "#5B2EFF" if app.current_screen == "schedule" else "#888888"
            on_release: app.go_to("schedule")

        MDLabel:
            text: "More"
            halign: "center"
            font_size: "11sp"
            size_hint_y: None
            height: "16dp"
            theme_text_color: "Custom"
            text_color: "#5B2EFF" if app.current_screen == "schedule" else "#888888"


# ==================================================
# SETTINGS SWITCH ROW TEMPLATE (icon + label + toggle)
# ==================================================

<SettingsSwitchRow@MDBoxLayout>:
    icon: ""
    text: ""
    size_hint_y: None
    height: "56dp"
    padding: "20dp", "0dp"
    spacing: "15dp"

    MDIcon:
        icon: root.icon
        pos_hint: {"center_y": .5}
        theme_text_color: "Custom"
        text_color: "#888888"

    MDLabel:
        text: root.text
        pos_hint: {"center_y": .5}

    MDSwitch:
        size_hint: None, None
        size: "36dp", "48dp"
        pos_hint: {"center_y": .5}


# ==================================================
# MAIN SCREEN
# ==================================================

<MainScreen>:
    name: "main"

    MDBoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            title: "Tuskanic Academy"
            elevation: 0
            left_action_items:
                [["menu", lambda x: nav_drawer.set_state("open")]]

        ScrollView:
            MDBoxLayout:
                orientation: "vertical"
                adaptive_height: True
                spacing: "15dp"
                padding: "15dp"

                # HERO CARD (responsive: stacks vertically on narrow phones)
                MDCard:
                    size_hint_y: None
                    height: "250dp" if Window.width >= dp(500) else "310dp"
                    radius: [30]
                    elevation: 8
                    md_bg_color: "#5B2EFF"
                    padding: "25dp"

                    MDBoxLayout:
                        orientation: "horizontal" if Window.width >= dp(500) else "vertical"

                        MDIcon:
                            icon: "school"
                            font_size: "120sp" if Window.width >= dp(500) else "70sp"
                            halign: "center"
                            theme_text_color: "Custom"
                            text_color: 1,1,1,1

                        MDBoxLayout:
                            orientation: "vertical"
                            spacing: "10dp"

                            Widget:

                            MDLabel:
                                text: "Learn Today,"
                                bold: True
                                font_style: "H3"
                                theme_text_color: "Custom"
                                text_color: 1,1,1,1

                            MDLabel:
                                text: "Go To Space Tomorrow With Tuskanic."
                                bold: True
                                font_style: "H4"
                                theme_text_color: "Custom"
                                text_color: 1,1,1,1

                            MDLabel:
                                text: "Best online and offline courses for your future."
                                theme_text_color: "Custom"
                                text_color: 1,1,1,0.9

                            MDRaisedButton:
                                text: "View Courses"
                                pos_hint: {"center_x": .5}
                                md_bg_color: 1,1,1,1
                                text_color: "#5B2EFF"
                                on_release: app.go_to("courses")

                # GRID CARDS (responsive: 2 columns on phones, 3 on tablets/desktop)
                GridLayout:
                    cols: 2 if Window.width < dp(600) else (3 if Window.width < dp(900) else 4)
                    spacing: "15dp"
                    adaptive_height: True
                    row_default_height: "180dp"
                    size_hint_y: None
                    height: self.minimum_height

                    MDCard:
                        radius: [25]
                        elevation: 5
                        ripple_behavior: True
                        padding: "15dp"
                        on_release: app.go_to("dashboard")
                        MDBoxLayout:
                            orientation: "vertical"
                            spacing: "10dp"
                            MDIcon:
                                icon: "view-dashboard"
                                halign: "center"
                                theme_text_color: "Custom"
                                text_color: "#4A6CF7"
                                font_size: "50sp"
                            MDLabel:
                                text: "Dashboard"
                                halign: "center"
                                bold: True
                            MDLabel:
                                text: "User account and courses"
                                halign: "center"
                                theme_text_color: "Secondary"

                    MDCard:
                        radius: [25]
                        elevation: 5
                        ripple_behavior: True
                        padding: "15dp"
                        on_release: app.go_to("courses")
                        MDBoxLayout:
                            orientation: "vertical"
                            spacing: "10dp"
                            MDIcon:
                                icon: "book-open-page-variant"
                                halign: "center"
                                theme_text_color: "Custom"
                                text_color: "#00C853"
                                font_size: "50sp"
                            MDLabel:
                                text: "Courses"
                                halign: "center"
                                bold: True
                            MDLabel:
                                text: "Explore academy courses"
                                halign: "center"
                                theme_text_color: "Secondary"

                    MDCard:
                        radius: [25]
                        elevation: 5
                        ripple_behavior: True
                        padding: "15dp"
                        on_release: app.go_to("teachers")
                        MDBoxLayout:
                            orientation: "vertical"
                            spacing: "10dp"
                            MDIcon:
                                icon: "account-group"
                                halign: "center"
                                theme_text_color: "Custom"
                                text_color: "#FF9800"
                                font_size: "50sp"
                            MDLabel:
                                text: "Teachers"
                                halign: "center"
                                bold: True
                            MDLabel:
                                text: "Professional teachers"
                                halign: "center"
                                theme_text_color: "Secondary"

                    MDCard:
                        radius: [25]
                        elevation: 5
                        ripple_behavior: True
                        padding: "15dp"
                        on_release: app.go_to("certificates")
                        MDBoxLayout:
                            orientation: "vertical"
                            spacing: "10dp"
                            MDIcon:
                                icon: "certificate"
                                halign: "center"
                                theme_text_color: "Custom"
                                text_color: "#FF4081"
                                font_size: "50sp"
                            MDLabel:
                                text: "Certificates"
                                halign: "center"
                                bold: True
                            MDLabel:
                                text: "Your certificates"
                                halign: "center"
                                theme_text_color: "Secondary"

                    MDCard:
                        radius: [25]
                        elevation: 5
                        ripple_behavior: True
                        padding: "15dp"
                        on_release: app.go_to("schedule")
                        MDBoxLayout:
                            orientation: "vertical"
                            spacing: "10dp"
                            MDIcon:
                                icon: "calendar"
                                halign: "center"
                                theme_text_color: "Custom"
                                text_color: "#7C4DFF"
                                font_size: "50sp"
                            MDLabel:
                                text: "Schedule"
                                halign: "center"
                                bold: True
                            MDLabel:
                                text: "Classes and events"
                                halign: "center"
                                theme_text_color: "Secondary"

                    MDCard:
                        radius: [25]
                        elevation: 5
                        ripple_behavior: True
                        padding: "15dp"
                        on_release: app.go_to("support")
                        MDBoxLayout:
                            orientation: "vertical"
                            spacing: "10dp"
                            MDIcon:
                                icon: "chat"
                                halign: "center"
                                theme_text_color: "Custom"
                                text_color: "#9C27B0"
                                font_size: "50sp"
                            MDLabel:
                                text: "Support"
                                halign: "center"
                                bold: True
                            MDLabel:
                                text: "Ask your questions"
                                halign: "center"
                                theme_text_color: "Secondary"

                # LOGIN CARD
                MDCard:
                    size_hint_y: None
                    height: "120dp"
                    radius: [30]
                    elevation: 8
                    md_bg_color: "#6C2BFF"
                    padding: "20dp"

                    MDBoxLayout:
                        spacing: "15dp"

                        MDIcon:
                            icon: "headphones"
                            font_size: "70sp"
                            theme_text_color: "Custom"
                            text_color: 1,1,1,1

                        MDBoxLayout:
                            orientation: "vertical"

                            MDLabel:
                                text: "Ready To Start Learning?"
                                bold: True
                                theme_text_color: "Custom"
                                text_color: 1,1,1,1

                            MDLabel:
                                text: "Login or create a new account."
                                theme_text_color: "Custom"
                                text_color: 1,1,1,0.9

                        MDRaisedButton:
                            text: "Login / Sign Up"
                            md_bg_color: 1,1,1,1
                            text_color: "#5B2EFF"
                            on_release: app.go_to("login")

                Widget:
                    size_hint_y: None
                    height: "10dp"

        BottomBar:

    MDNavigationDrawer:
        id: nav_drawer

        MDBoxLayout:
            orientation: "vertical"

            # HEADER
            MDBoxLayout:
                orientation: "vertical"
                size_hint_y: None
                height: "130dp"
                padding: "20dp"
                spacing: "5dp"
                md_bg_color: "#5B2EFF"

                MDIcon:
                    icon: "account-circle"
                    font_size: "48sp"
                    theme_text_color: "Custom"
                    text_color: 1, 1, 1, 1

                MDLabel:
                    text: "Settings"
                    bold: True
                    font_style: "H5"
                    theme_text_color: "Custom"
                    text_color: 1, 1, 1, 1

            # SETTINGS LIST (Telegram style)
            ScrollView:
                MDList:

                    OneLineIconListItem:
                        text: "My Account"
                        on_release:
                            nav_drawer.set_state("close")
                            app.go_to("account")
                        IconLeftWidget:
                            icon: "account-outline"

                    OneLineIconListItem:
                        text: "Notifications and Sounds"
                        on_release:
                            nav_drawer.set_state("close")
                            app.go_to("chat_notifications")
                        IconLeftWidget:
                            icon: "bell-outline"

                    OneLineIconListItem:
                        text: "Language"
                        on_release:
                            nav_drawer.set_state("close")
                            app.go_to("language")
                        IconLeftWidget:
                            icon: "web"

                    OneLineIconListItem:
                        text: "Chat Settings"
                        on_release:
                            nav_drawer.set_state("close")
                            app.go_to("chat_settings")
                        IconLeftWidget:
                            icon: "chat-outline"

                    OneLineIconListItem:
                        text: "Privacy and Security"
                        on_release:
                            nav_drawer.set_state("close")
                            app.go_to("privacy")
                        IconLeftWidget:
                            icon: "shield-lock-outline"

                    OneLineIconListItem:
                        text: "Help"
                        on_release:
                            nav_drawer.set_state("close")
                            app.go_to("support")
                        IconLeftWidget:
                            icon: "help-circle-outline"

            # DARK / LIGHT MODE — single on/off switch, Telegram style
            MDBoxLayout:
                size_hint_y: None
                height: "56dp"
                padding: "20dp", "0dp"
                spacing: "15dp"

                MDIcon:
                    icon: "theme-light-dark"
                    pos_hint: {"center_y": .5}
                    theme_text_color: "Custom"
                    text_color: "#888888"

                MDLabel:
                    text: "Dark Mode"
                    pos_hint: {"center_y": .5}

                ThemeSwitch:
                    id: dark_mode_switch
                    pos_hint: {"center_y": .5}
                    on_active: app.toggle_theme(self.active)


# ==================================================
# DASHBOARD
# ==================================================

<DashboardScreen>:
    name: "dashboard"

    MDBoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            title: "Dashboard"
            elevation: 0
            left_action_items:
                [["arrow-left", lambda x: app.go_back()]]

        MDLabel:
            text: "Dashboard Page"
            halign: "center"

        Widget:

        BottomBar:


# ==================================================
# COURSES
# ==================================================

<CoursesScreen>:
    name: "courses"

    MDBoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            title: "Courses"
            elevation: 0
            left_action_items:
                [["arrow-left", lambda x: app.go_back()]]

        MDLabel:
            text: "Courses Page"
            halign: "center"

        Widget:

        BottomBar:


# ==================================================
# TEACHERS
# ==================================================

<TeachersScreen>:
    name: "teachers"

    MDBoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            title: "Teachers"
            elevation: 0
            left_action_items:
                [["arrow-left", lambda x: app.go_back()]]

        MDLabel:
            text: "Teachers Page"
            halign: "center"

        Widget:

        BottomBar:


# ==================================================
# CERTIFICATES
# ==================================================

<CertificatesScreen>:
    name: "certificates"

    MDBoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            title: "Certificates"
            elevation: 0
            left_action_items:
                [["arrow-left", lambda x: app.go_back()]]

        MDLabel:
            text: "Certificates Page"
            halign: "center"

        Widget:

        BottomBar:


# ==================================================
# SCHEDULE
# ==================================================

<ScheduleScreen>:
    name: "schedule"

    MDBoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            title: "Schedule"
            elevation: 0
            left_action_items:
                [["arrow-left", lambda x: app.go_back()]]

        MDLabel:
            text: "Schedule Page"
            halign: "center"

        Widget:

        BottomBar:


# ==================================================
# SUPPORT
# ==================================================

<SupportScreen>:
    name: "support"

    MDBoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            title: "Help & Support"
            elevation: 0
            left_action_items:
                [["arrow-left", lambda x: app.go_back()]]

        ScrollView:
            MDBoxLayout:
                orientation: "vertical"
                adaptive_height: True
                padding: "20dp"
                spacing: "15dp"

                MDLabel:
                    text: "Frequently Asked Questions"
                    bold: True
                    font_style: "Subtitle1"
                    size_hint_y: None
                    height: self.texture_size[1]

                MDList:
                    OneLineIconListItem:
                        text: "How do I enroll in a course?"
                        IconLeftWidget:
                            icon: "help-circle-outline"

                    OneLineIconListItem:
                        text: "How do I get my certificate?"
                        IconLeftWidget:
                            icon: "help-circle-outline"

                    OneLineIconListItem:
                        text: "How do I reset my password?"
                        IconLeftWidget:
                            icon: "help-circle-outline"

                    OneLineIconListItem:
                        text: "How do I contact a teacher?"
                        IconLeftWidget:
                            icon: "help-circle-outline"

                MDRaisedButton:
                    text: "Contact Support"
                    pos_hint: {"center_x": .5}
                    md_bg_color: "#5B2EFF"

        BottomBar:


# ==================================================
# LOGIN
# ==================================================

<LoginScreen>:
    name: "login"

    MDBoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            title: "Login"
            elevation: 0
            left_action_items:
                [["arrow-left", lambda x: app.go_back()]]

        MDBoxLayout:
            orientation: "vertical"

            Widget:

            MDLabel:
                text: "Login"
                halign: "center"
                font_style: "H4"

            MDRaisedButton:
                text: "Go To Sign Up"
                pos_hint: {"center_x": .5}
                on_release: app.go_to("signup")

            Widget:

        BottomBar:


# ==================================================
# SIGNUP
# ==================================================

<SignupScreen>:
    name: "signup"

    MDBoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            title: "Sign Up"
            elevation: 0
            left_action_items:
                [["arrow-left", lambda x: app.go_back()]]

        MDBoxLayout:
            orientation: "vertical"

            Widget:

            MDLabel:
                text: "Sign Up"
                halign: "center"
                font_style: "H4"

            Widget:

        BottomBar:


# ==================================================
# SETTINGS SUB-PAGES
# ==================================================

<AccountScreen>:
    name: "account"

    MDBoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            title: "My Account"
            elevation: 0
            left_action_items:
                [["arrow-left", lambda x: app.go_back()]]

        ScrollView:
            MDBoxLayout:
                orientation: "vertical"
                adaptive_height: True
                padding: "20dp"
                spacing: "20dp"

                # PROFILE HEADER
                MDBoxLayout:
                    orientation: "vertical"
                    adaptive_height: True
                    spacing: "8dp"

                    MDIcon:
                        icon: "account-circle"
                        halign: "center"
                        valign: "middle"
                        text_size: self.width, None
                        size_hint_y: None
                        height: dp(90) if Window.width >= dp(500) else dp(72)
                        font_size: "80sp" if Window.width >= dp(500) else "64sp"
                        theme_text_color: "Custom"
                        text_color: "#5B2EFF"

                    MDLabel:
                        text: "Guest User"
                        halign: "center"
                        valign: "middle"
                        text_size: self.width, None
                        size_hint_y: None
                        height: self.texture_size[1] + dp(4)
                        bold: True
                        font_style: "H6"

                    MDLabel:
                        text: "guest@tuskanic.academy"
                        halign: "center"
                        valign: "middle"
                        text_size: self.width, None
                        size_hint_y: None
                        height: self.texture_size[1] + dp(4)
                        theme_text_color: "Secondary"

                MDList:
                    OneLineIconListItem:
                        text: "Edit Name"
                        IconLeftWidget:
                            icon: "account-edit-outline"

                    OneLineIconListItem:
                        text: "Change Email"
                        IconLeftWidget:
                            icon: "email-outline"

                    OneLineIconListItem:
                        text: "Change Password"
                        IconLeftWidget:
                            icon: "lock-outline"

                    OneLineIconListItem:
                        text: "Log Out"
                        theme_text_color: "Custom"
                        text_color: "#E53935"
                        IconLeftWidget:
                            icon: "logout"
                            theme_text_color: "Custom"
                            text_color: "#E53935"

        BottomBar:


<ChatNotificationsScreen>:
    name: "chat_notifications"

    MDBoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            title: "Notifications and Sounds"
            elevation: 0
            left_action_items:
                [["arrow-left", lambda x: app.go_back()]]

        ScrollView:
            MDBoxLayout:
                orientation: "vertical"
                adaptive_height: True
                padding: "0dp", "10dp"
                spacing: "5dp"

                SettingsSwitchRow:
                    icon: "message-badge-outline"
                    text: "Message Notifications"

                SettingsSwitchRow:
                    icon: "book-open-variant"
                    text: "Course Reminders"

                SettingsSwitchRow:
                    icon: "volume-high"
                    text: "Sound"

                SettingsSwitchRow:
                    icon: "vibrate"
                    text: "Vibrate"

        Widget:

        BottomBar:


<LanguageScreen>:
    name: "language"

    MDBoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            title: "Language"
            elevation: 0
            left_action_items:
                [["arrow-left", lambda x: app.go_back()]]

        ScrollView:
            MDList:
                OneLineIconListItem:
                    text: "English"
                    on_release: app.set_language("English")
                    IconLeftWidget:
                        icon: "radiobox-marked" if app.selected_language == "English" else "radiobox-blank"
                        theme_text_color: "Custom"
                        text_color: "#5B2EFF" if app.selected_language == "English" else "#888888"

                OneLineIconListItem:
                    text: "فارسی (Persian)"
                    on_release: app.set_language("Persian")
                    IconLeftWidget:
                        icon: "radiobox-marked" if app.selected_language == "Persian" else "radiobox-blank"
                        theme_text_color: "Custom"
                        text_color: "#5B2EFF" if app.selected_language == "Persian" else "#888888"

                OneLineIconListItem:
                    text: "العربية (Arabic)"
                    on_release: app.set_language("Arabic")
                    IconLeftWidget:
                        icon: "radiobox-marked" if app.selected_language == "Arabic" else "radiobox-blank"
                        theme_text_color: "Custom"
                        text_color: "#5B2EFF" if app.selected_language == "Arabic" else "#888888"

        Widget:

        BottomBar:


<ChatSettingsScreen>:
    name: "chat_settings"

    MDBoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            title: "Chat Settings"
            elevation: 0
            left_action_items:
                [["arrow-left", lambda x: app.go_back()]]

        ScrollView:
            MDBoxLayout:
                orientation: "vertical"
                adaptive_height: True
                padding: "0dp", "10dp"
                spacing: "5dp"

                SettingsSwitchRow:
                    icon: "check-all"
                    text: "Read Receipts"

                SettingsSwitchRow:
                    icon: "dots-horizontal"
                    text: "Typing Indicator"

                SettingsSwitchRow:
                    icon: "download-outline"
                    text: "Auto-Download Media"

                SettingsSwitchRow:
                    icon: "keyboard-return"
                    text: "Enter to Send"

        Widget:

        BottomBar:


<PrivacyScreen>:
    name: "privacy"

    MDBoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            title: "Privacy and Security"
            elevation: 0
            left_action_items:
                [["arrow-left", lambda x: app.go_back()]]

        ScrollView:
            MDList:
                OneLineIconListItem:
                    text: "Delete My Account"
                    theme_text_color: "Custom"
                    text_color: "#E53935"
                    IconLeftWidget:
                        icon: "delete-outline"
                        theme_text_color: "Custom"
                        text_color: "#E53935"

        Widget:

        BottomBar:

'''


class MainScreen(MDScreen):
    pass

class DashboardScreen(MDScreen):
    pass

class CoursesScreen(MDScreen):
    pass

class TeachersScreen(MDScreen):
    pass

class CertificatesScreen(MDScreen):
    pass

class ScheduleScreen(MDScreen):
    pass

class SupportScreen(MDScreen):
    pass

class LoginScreen(MDScreen):
    pass

class SignupScreen(MDScreen):
    pass

class AccountScreen(MDScreen):
    pass

class ChatNotificationsScreen(MDScreen):
    pass

class LanguageScreen(MDScreen):
    pass

class ChatSettingsScreen(MDScreen):
    pass

class PrivacyScreen(MDScreen):
    pass


class TuskanicApp(MDApp):

    # tracks the active tab/screen so the bottom bar can highlight it;
    # exists on the App itself (never None) so KV bindings never crash
    # before app.root has been created
    current_screen = StringProperty("main")
    selected_language = StringProperty("English")

    def build(self):
        self.theme_cls.primary_palette = "DeepPurple"
        self.theme_cls.theme_style = "Light"

        # navigation history (used for the phone hardware/ESC back button)
        self.history = ["main"]

        # make the phone's hardware back button (Android) and the
        # desktop ESC key navigate back inside the app instead of
        # closing the window/app
        Window.bind(on_keyboard=self.on_key_back)

        return Builder.load_string(KV)

    def on_start(self):
        # sync the switch with the current theme once, after everything is
        # built -- doing this in KV directly caused the switch to fight with
        # the binding and stop responding to taps.
        #
        # IMPORTANT: this must be delayed to the next frame with
        # Clock.schedule_once. Setting `.active` right here, synchronously,
        # happens before Kivy has finished laying out the widget tree, so
        # the switch's thumb still thinks its own width is 0 (or a
        # placeholder). It then calculates and freezes the thumb's
        # position using that wrong width, and the thumb stays visually
        # broken/detached from the track forever after -- every future
        # tap just animates starting from that broken spot, which is why
        # the white ball can end up "anywhere". Scheduling this for the
        # next frame lets layout finish first, so the width is correct.
        Clock.schedule_once(self._sync_dark_mode_switch, 0)

    def _sync_dark_mode_switch(self, dt):
        try:
            self.root.get_screen("main").ids.dark_mode_switch.active = (
                self.theme_cls.theme_style == "Dark"
            )
        except Exception:
            pass

    def on_key_back(self, window, key, *args):
        if key == 27:  # ESC on desktop / hardware back button on Android
            if len(self.history) > 1:
                self.go_back()
                return True  # consume the event, don't close the app
            return False  # already on the main screen -> let the OS handle it
        return False

    def go_to(self, screen):
        if not self.history or self.history[-1] != screen:
            self.history.append(screen)
        self.root.current = screen
        self.current_screen = screen

    def go_back(self):
        if len(self.history) > 1:
            self.history.pop()
            self.root.current = self.history[-1]
            self.current_screen = self.history[-1]

    def set_dark(self):
        self.theme_cls.theme_style = "Dark"

    def set_light(self):
        self.theme_cls.theme_style = "Light"

    def toggle_theme(self, is_dark):
        """Single on/off switch for Dark Mode (Telegram-style settings)."""
        self.theme_cls.theme_style = "Dark" if is_dark else "Light"

    def set_language(self, language):
        self.selected_language = language

TuskanicApp().run()