# TODO AFTER EVERYTHING IS DONE
# AT BEGINNING OF INITIALIZATION PUT SUBMIT BUTTON OFF THE SCREEN
#   THEN ONCE ADD TASK IS PRESSED PUT IT ON SCREEN
#       ONCE SUBMIT IS PRESSED, PUT IT BACK OFF SCREEN AGAIN FOR NEXT ROUND
# EVERY TIME ADD TASK IS PRESSED OR SUBMIT IS PRESSED, RESET EVENT AND DESCRIPTION TO EMPTY


import time
import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton,
                             QLabel, QStackedWidget, QLineEdit, QCalendarWidget,
                             QSplashScreen, QMainWindow, QMessageBox, QDateTimeEdit,
                             QScrollArea, QSpinBox, QComboBox, QTimeEdit, QListWidget,
                             QTextBrowser, QProgressBar, QFrame, QVBoxLayout)
from PyQt6.QtGui import QIcon, QFont, QFontDatabase, QPixmap, QColor, QPalette, QCursor
from PyQt6.QtCore import Qt, QDate, QTimer

from itertools import permutations

userInfo = {"Activity": [], "Description": [], "Hours": [], "Day": []}
available_hours = {}
tasks = {}
descriptionsGlob = {}
schedulesArr = []
completeSchedule = {"Monday": "", "Tuesday": "", "Wednesday": "", "Thursday": "", "Friday": "", "Saturday": "",
                    "Sunday": ""}
scheduleIndex = 0
eventsAdded = 0


class Page1(QWidget):
    def __init__(self, page2):
        super().__init__()

        self.page2 = page2

        taskMateLabel = QLabel("Task Mate", self)
        taskMateLabel.setFont(QFont("Trebuchet MS", 30))
        taskMateLabel.setStyleSheet("""
                    QLabel {
                        color: black;
                        background: rgba(0,0,0,0);
                    }
                """)
        taskMateLabel.move(400, 20)

        # Font Size
        # headerFont = QFont()
        # headerFont.setBold(True)
        # headerFont.setPointSize(20)

        # Font Color
        # taskMateLabel.setFont(headerFont)
        # taskMateLabel.setStyleSheet("color: black")

        # Create Event
        eventLabel = QLabel("Event Name", self)
        eventLabel.setFont(QFont("Tahoma", 14))
        eventLabel.move(50, 100)
        eventLabel.setStyleSheet("""
                    QLabel {
                        color: black;
                        background: rgba(0,0,0,0);
                    }
                """)

        # Textbox for Event Name
        eventTextBox = QLineEdit(self)
        eventTextBox.setObjectName("ModernLineEdit1")
        eventTextBox.setStyleSheet("""
                    QLineEdit#ModernLineEdit1 {
                        background-color: #F5F5F5;
                        border: none;
                        padding: 8px;
                        border-radius: 8px;
                    }
                    QLineEdit#ModernLineEdit:hover {
                        background-color: #E6E6E6;
                    }
                    QLineEdit#ModernLineEdit:focus {
                        background-color: white;
                        border: 2px solid #3498DB;
                    }
                """)
        eventTextBox.move(160, 100)
        eventTextBox.setFixedWidth(200)
        eventTextBox.setFixedHeight(33)

        # Hours
        hoursLabel = QLabel("How many hours for this task?", self)
        hoursLabel.setFont(QFont("Tahoma", 14))
        hoursLabel.setStyleSheet("""
                    QLabel {
                        color: black;
                        background: rgba(0,0,0,0);
                    }
                """)
        hoursLabel.move(50, 155)

        hoursBox = QSpinBox(self)
        hoursBox.setStyleSheet(
            """
                QSpinBox {
                    background-color: #FFF3E2;
                    color: #333333;
                    border: 2px solid #FA9884;
                    border-radius: 5px;
                    padding: 2px;
                }
            """
        )
        hoursBox.move(50, 185)

        # Day of the Week
        dayLabel = QLabel("Which day would you like to do the task?", self)
        dayLabel.setFont(QFont("Tahoma", 14))
        dayLabel.setStyleSheet("""
                    QLabel {
                        color: black;
                        background: rgba(0,0,0,0);
                    }
                """)
        dayLabel.move(360, 230)

        # Styles for QComboBox
        styleCombo = f"""
                    QComboBox {{
                        border-radius: 8px;
                        border: 2px solid rgb(25, 167, 206);
                        padding: 4px;
                        background-color: rgb(175, 211, 226);
                    }}
                    QComboBox::drop-down {{
                        subcontrol-origin: padding;
                        subcontrol-position: top right;
                        width: 24px;
                        border-top-right-radius: 8px;
                        border-bottom-right-radius: 8px;
                        border: none;
                    }}
                    QComboBox::down-arrow {{
                        image: url(down_arrow.png);
                        width: 24px;
                        height: 24px;
                    }}
                    QComboBox QAbstractItemView {{

                        border-radius: 8px;
                        border: 2px solid rgb(25, 167, 206);
                        padding: 4px;
                        background-color: rgb(175, 211, 226);
                    }}
                    QComboBox QAbstractItemView::item {{
                        height: 30px;
                        padding: 4px;
                    }}
                    QComboBox QAbstractItemView::item:hover {{
                        background-color: rgb(60, 60, 60);
                    }}
                """

        dayComboBox = QComboBox(self)
        dayComboBox.setStyleSheet(styleCombo)
        dayComboBox.addItems(["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"])
        dayComboBox.move(360, 265)
        dayComboBox.textActivated[str].connect(self.onActivated)

        self.dayText = QLabel('Sunday', self)
        self.dayText.move(-5000, -5000)

        # Time Available
        timeLabel = QLabel("Which hours are you available?", self)
        timeLabel.setFont(QFont("Tahoma", 14))
        timeLabel.setStyleSheet("""
                    QLabel {
                        color: black;
                        background: rgba(0,0,0,0);
                    }
                """)
        timeLabel.move(50, 230)

        fromTimeEdit = QTimeEdit(self)
        fromTimeEdit.setDisplayFormat("HH:mm")
        fromTimeEdit.setStyleSheet(
            """
                QTimeEdit {
                    background-color: #FFF3E2;
                    color: #333333;
                    border: 2px solid #FA9884;
                    border-radius: 5px;
                    padding: 2px;
                }
            """
        )
        fromTimeEdit.move(50, 265)

        toLabel = QLabel("to", self)
        toLabel.setStyleSheet("""
                    QLabel {
                        color: black;
                        background: rgba(0,0,0,0);
                    }
                """)
        toLabel.move(125, 267)

        toTimeEdit = QTimeEdit(self)
        toTimeEdit.move(150, 265)
        toTimeEdit.setDisplayFormat("HH:mm")
        toTimeEdit.setStyleSheet(
            """
                QTimeEdit {
                    background-color: #FFF3E2;
                    color: #333333;
                    border: 2px solid #FA9884;
                    border-radius: 5px;
                    padding: 2px;
                }
            """
        )

        # Descriptions
        descriptionLabel = QLabel("Notes or Descriptions", self)
        descriptionLabel.setFont(QFont("Tahoma", 14))
        descriptionLabel.setStyleSheet("""
                    QLabel {
                        color: black;
                        background: rgba(0,0,0,0);
                    }
                """)
        descriptionLabel.move(50, 320)

        # Textbox for Note and Description
        descriptionTextBox = QLineEdit(self)
        descriptionTextBox.setObjectName("ModernLineEdit1")
        descriptionTextBox.setStyleSheet("""
                            QLineEdit#ModernLineEdit1 {
                                background-color: #F5F5F5;
                                border: none;
                                padding: 8px;
                                border-radius: 8px;
                            }
                            QLineEdit#ModernLineEdit:hover {
                                background-color: #E6E6E6;
                            }
                            QLineEdit#ModernLineEdit:focus {
                                background-color: white;
                                border: 2px solid #3498DB;
                            }
                        """)
        descriptionTextBox.move(50, 350)
        descriptionTextBox.setFixedWidth(300)
        descriptionTextBox.setFixedHeight(150)

        # Add Task
        addTaskButton = QPushButton("Add Task", self)
        addTaskButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        addTaskButton.setObjectName("ModernButton")
        addTaskButton.setStyleSheet("""
                    QPushButton#ModernButton {
                        background-color: #2ECC71;
                        color: white;
                        border: none;
                        padding: 8px 16px;
                        border-radius: 16px;
                    }
                    QToolButton#ModernButton:hover {
                        background-color: #27AE60;
                    }
                    QToolButton#ModernButton:pressed {
                        background-color: #1E8449;
                    }
                """)
        addTaskButton.move(50, 530)
        addTaskButton.clicked.connect(
            lambda: self.addTask(eventTextBox, descriptionTextBox, hoursBox, fromTimeEdit, toTimeEdit, dayLabel,
                                 dayComboBox, timeLabel, toLabel))

        # Submit
        submitButton = QPushButton("Submit", self)
        submitButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        submitButton.setObjectName("ModernButton2")
        submitButton.setStyleSheet("""
                    QPushButton#ModernButton2 {
                        background-color: #3498DB;
                        color: white;
                        border: none;
                        padding: 8px 16px;
                        border-radius: 16px;
                    }
                    QToolButton#ModernButton:hover {
                        background-color: #2980B9;
                    }
                    QToolButton#ModernButton:pressed {
                        background-color: #1B4F72;
                    }
                """)
        submitButton.move(200, 530)
        submitButton.clicked.connect(
            lambda: self.goToPage2(dayLabel, dayComboBox, timeLabel, fromTimeEdit, toTimeEdit, toLabel))

        # Set app background
        # self.setStyleSheet("background-image: url('app_bg.jpg');")
        # self.setStyleSheet("background-color: #FEE8B0;")

        # Set developer notes
        changelogButton = QPushButton("?", self)
        changelogButton.clicked.connect(lambda: QMessageBox.information(None, '', 'Version 1.0 (March 7th, 2023)'
                                                                                  '\n'
                                                                                  '\n- Task creation page developed with limited UI elements'
                                                                                  '\n- User input validation'
                                                                                  '\n- Multiple task creation capabilities added'
                                                                                  '\n- Checkbox integration for days of the week'
                                                                                  '\n- Console log output for task management for the time being'))
        changelogButton.move(800, 560)

    def onActivated(self, text):
        self.dayText.setText(text)
        self.dayText.adjustSize()

    def addTask(self, eventTextBox, descriptionTextBox, hoursBox, fromTimeEdit, toTimeEdit, dayLabel, dayComboBox,
                timeLabel, toLabel):
        global eventsAdded

        if not self.validate_inputs(eventTextBox, hoursBox, descriptionTextBox, fromTimeEdit, toTimeEdit):
            return

        dayLabel.move(-5000, -5000)
        dayComboBox.move(-5000, -5000)
        timeLabel.move(-5000, -5000)
        fromTimeEdit.move(-5000, -5000)
        toTimeEdit.move(-5000, -5000)
        toLabel.move(-5000, -5000)

        event = eventTextBox.text()
        description = descriptionTextBox.text()
        hours = hoursBox.text()
        day = self.dayText.text()
        fromTime = int(fromTimeEdit.text()[:2])
        toTime = int(toTimeEdit.text()[:2])

        userInfo["Activity"].append(event)
        userInfo["Description"].append(description)
        userInfo["Hours"].append(hours)
        userInfo["Day"].append(day)

        descriptionsGlob[event] = description

        available_hours[day] = (fromTime, toTime)

        tasks[event] = int(hours)

        eventsAdded += 1

        # print(eventsAdded)
        # print(available_hours)
        # print(f"{fromTime} -> {toTime}")
        # print(hours)
        # print(event)
        # print(description)
        # print(day)

    def goToPage2(self, dayLabel, dayComboBox, timeLabel, fromTimeEdit, toTimeEdit, toLabel):

        self.generateSchedule()

        self.page2.updateScheduleList()

        stacked_widget.setCurrentWidget(page2)

        dayLabel.move(360, 230)
        dayComboBox.move(360, 265)
        timeLabel.move(50, 230)
        fromTimeEdit.move(50, 265)
        toTimeEdit.move(150, 265)
        toLabel.move(125, 267)

        print(userInfo)

    def generateSchedule(self):
        # generate all possible task orders
        task_orders = permutations(tasks.keys())

        # generate all possible schedules for each day
        schedules = {}
        for day, hours in available_hours.items():
            schedules[day] = []
            for task_order in task_orders:
                schedule = {}
                current_time = hours[0]
                for task in task_order:
                    duration = tasks[task]
                    if current_time + duration > hours[1]:
                        break
                    schedule[task] = (current_time, current_time + duration)
                    current_time += duration
                else:
                    schedules[day].append(schedule)

        # print all possible schedules for each day
        for day, day_schedules in schedules.items():
            print(f"{day}:")  # this will be a label above the listview
            if len(day_schedules) == 0:
                print("  No valid schedules found.")
            else:
                for i, schedule in enumerate(day_schedules):
                    print(f"  Schedule {i + 1}:")
                    for task, (start_time, end_time) in schedule.items():

                        if (len(schedulesArr) > i):
                            schedulesArr[i] += f"{task}->{start_time}:00-{end_time}:00\n"
                        else:
                            schedulesArr.append(f"{task}->{start_time}:00-{end_time}:00\n")

                        print(f"    {task}: {start_time}-{end_time}")
                    print()
                    schedulesArr[-1] = schedulesArr[-1][:-1]
                    print(schedulesArr)

    def validate_inputs(self, eventTextBox, hoursBox, descriptionTextBox, fromTimeEdit, toTimeEdit):
        event = eventTextBox.text()
        hours = hoursBox.value()
        description = descriptionTextBox.text()
        from_time = int(fromTimeEdit.text()[:2])
        to_time = int(toTimeEdit.text()[:2])

        if not event:
            QMessageBox.warning(self, "Invalid input", "Event name cannot be empty.")
            return False

        if hours <= 0:
            QMessageBox.warning(self, "Invalid input", "Hours must be greater than 0.")
            return False

        if from_time >= to_time:
            QMessageBox.warning(self, "Invalid input", "Start time must be less than finish time.")
            return False

        if not description:
            QMessageBox.warning(self, "Invalid input", "Description cannot be empty.")
            return False

        return True


# Pop up window


# Page 2
class Page2(QWidget):
    def __init__(self, page3):
        super().__init__()

        self.page3 = page3

        scheduleLabel = QLabel("Choose Your Schedule", self)
        scheduleLabel.setFont(QFont("Tahoma", 25))
        scheduleLabel.setStyleSheet("""
                    QLabel {
                        color: black;
                        background: rgba(0,0,0,0);
                    }
                """)
        scheduleLabel.move(490, 100)

        self.dayLabel = QLabel("", self)
        self.dayLabel.setFont(QFont("Tahoma", 20))
        self.dayLabel.setStyleSheet("""
                    QLabel {
                        color: black;
                        background: rgba(0,0,0,0);
                    }
                """)
        self.dayLabel.move(610, 200)

        # Font
        headerFont = QFont()
        headerFont.setBold(True)
        headerFont.setPointSize(30)

        # Set Font
        scheduleLabel.setFont(headerFont)

        # Currently generates schedule, will change to auto do on page load or make it the submit button from page 1
        submitButton = QPushButton("next", self)
        submitButton.setObjectName("ModernButton2")
        submitButton.setStyleSheet("""
                    QPushButton#ModernButton2 {
                        background-color: #3498DB;
                        color: white;
                        border: none;
                        padding: 8px 16px;
                        border-radius: 16px;
                    }
                    QToolButton#ModernButton:hover {
                        background-color: #2980B9;
                    }
                    QToolButton#ModernButton:pressed {
                        background-color: #1B4F72;
                    }
                """)
        submitButton.move(620, 600)

        submitButton.clicked.connect(self.goToPage3)
        # button.clicked.connect(self.generateSchedule)

        # Load schedule
        self.scheduleList = QListWidget(self)
        self.setStyleSheet("""
                    QListWidget {
                        background: rgba(0,0,0,0);
                        background-color: #F1F6F9;
                        border: 1px #394867;
                        font-family: Arial;
                        font-size: 18px;
                        border-radius: 16px;
                    }
                    QListWidget::item {
                        background: rgba(0,0,0,0);
                        background-color: #F6F1E9;
                        color: black;
                        padding: 5px;
                        border-radius: 16px;
                    }
                    QListWidget::item:selected {
                        background: rgba(0,0,0,0);
                        background-color: #088395;
                        color: white;
                        border-radius: 16px;
                    }
                """)
        # self.scheduleList.move(550, 250)
        self.scheduleList.setGeometry(450, 250, 400, 300)
        self.scheduleList.currentItemChanged.connect(self.indexChanged)
        # self.scheduleList.currentItemChanged.connect(self.textChanged)

    def textChanged(self, i):
        # Gets the text of the selected schedule
        print("indexChanged")
        print(i.text())

    def indexChanged(self, current, previous):
        # Gets the index of the selected schedule
        global scheduleIndex

        print("textChanged")
        print(self.scheduleList.row(current))
        scheduleIndex = self.scheduleList.row(current)

    def updateScheduleList(self):
        self.scheduleList.clear()
        self.scheduleList.addItems(schedulesArr)
        self.dayLabel.setText(userInfo["Day"][0])

    def goToPage3(self):
        self.page3.updateCalendar()
        stacked_widget.setCurrentWidget(page3)


class Page3(QWidget):
    def __init__(self):
        super().__init__()

        scheduleLabel = QLabel("Your Schedule", self)
        scheduleLabel.setStyleSheet("""
                    QLabel {
                        color: black;
                        background: rgba(0,0,0,0);
                    }
                """)
        scheduleLabel.move(540, 100)

        # Font
        font1 = QFont()
        font1.setBold(True)
        font1.setPointSize(30)

        # Set Font
        scheduleLabel.setFont(font1)

        # Calendar View
        self.calendarView = QCalendarWidget(self)
        self.calendarView.setSelectedDate(self.calendarView.selectedDate())
        self.calendarView.setStyleSheet("""
                                    QCalendarWidget QToolButton {
                                        height: 50px;
                                        width: 80px;
                                        color: white;
                                        font-size: 24px;
                                        icon-size: 56px, 56px;
                                        background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop: 0 #3F52BD, stop: 1 #CA4683); 
                                    }
                                    QCalendarWidget QMenu {
                                        width: 150px;
                                        left: 20px;
                                        color: white;
                                        font-size: 18px;
                                        background-color: rgb(255, 255, 255);
                                    }
                                    QCalendarWidget QSpinBox { 
                                        width: 150px; 
                                        font-size:24px; 
                                        color: white; 
                                        background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop: 0 #3F52BD, stop: 1 #CA4683); 
                                        selection-background-color: rgb(255, 255, 255);
                                        selection-color: rgb(255, 255, 255);
                                    }
                                    QCalendarWidget QSpinBox::up-button { subcontrol-origin: border;  subcontrol-position: top right;  width:65px; }
                                    QCalendarWidget QSpinBox::down-button {subcontrol-origin: border; subcontrol-position: bottom right;  width:65px;}
                                    QCalendarWidget QSpinBox::up-arrow { width:56px;  height:56px; }
                                    QCalendarWidget QSpinBox::down-arrow { width:56px;  height:56px; }

                                    /* header row */
                                    QCalendarWidget QWidget { alternate-background-color: rgb(255, 255, 255); }

                                    /* normal days */
                                    QCalendarWidget QAbstractItemView:enabled 
                                    {
                                        font-size:24px;  
                                        color: rgb(180, 180, 180);  
                                        background-color: white;  
                                        selection-background-color: black; 
                                        selection-color: rgb(0, 255, 0); 
                                    }

                                    /* days in other months */
                                    /* navigation bar */
                                    QCalendarWidget QWidget#qt_calendar_navigationbar
                                    { 
                                    background-color:qlineargradient(x1:0, y1:0, x2:0, y2:1, stop: 0 #3F52BD, stop: 1 #CA4683); ; 
                                    }

                                    QCalendarWidget QAbstractItemView:disabled 
                                    { 
                                    color: rgb(255, 255, 255); 
                                    }
                                """)
        self.calendarView.move(400, 250)
        self.calendarView.clicked.connect(self.on_date_clicked)

        # Description Selected TextBox
        self.descriptionTextBrowser = QTextBrowser(self)
        self.descriptionTextBrowser.setStyleSheet("""
                                    QTextBrowser {
                                        background: rgba(0,0,0,0);
                                        background-color: #F1F6F9;
                                        border: 1px #394867;
                                        font-family: Arial;
                                        font-size: 18px;
                                        color: black;
                                        border-radius: 16px;
                                    }
                                    QListWidget::item {
                                        background: rgba(0,0,0,0);
                                        background-color: #F6F1E9;
                                        padding: 5px;
                                        color: black;
                                        border-radius: 16px;
                                    }
                                    QListWidget::item:selected {
                                        background: rgba(0,0,0,0);
                                        background-color: #088395;
                                        color: white;
                                        border-radius: 16px;
                                    }
                                """)
        # self.descriptionTextBrowser.move(600, 150)
        self.descriptionTextBrowser.setGeometry(920, 250, 300, 310)

        # Schedule List Trial
        self.scheduleListCal = QListWidget(self)
        self.scheduleListCal.setStyleSheet("""
                            QListWidget {
                                background: rgba(0,0,0,0);
                                background-color: #F1F6F9;
                                border: 1px #394867;
                                font-family: Arial;
                                font-size: 18px;
                                border-radius: 16px;
                            }
                            QListWidget::item {
                                background: rgba(0,0,0,0);
                                background-color: #F6F1E9;
                                padding: 5px;
                                color: black;
                                border-radius: 16px;
                            }
                            QListWidget::item:selected {
                                background: rgba(0,0,0,0);
                                background-color: #088395;
                                color: white;
                                border-radius: 16px;
                            }
                        """)
        # self.scheduleListCal.move(10, 150)
        self.scheduleListCal.setGeometry(50, 250, 300, 310)
        self.scheduleListCal.currentItemChanged.connect(self.indexChanged)

        button = QPushButton("Back", self)
        button.setObjectName("ModernButton2")
        button.setStyleSheet("""
                            QPushButton#ModernButton2 {
                                background-color: #3498DB;
                                color: white;
                                border: none;
                                padding: 8px 16px;
                                border-radius: 16px;
                            }
                            QToolButton#ModernButton:hover {
                                background-color: #2980B9;
                            }
                            QToolButton#ModernButton:pressed {
                                background-color: #1B4F72;
                            }
                        """)
        button.move(50, 650)
        button.clicked.connect(self.go_to_page1)

    def updateCalendar(self):
        global scheduleIndex
        global eventsAdded

        print("CALENDAR")

        newSchedules = []
        activity = ""
        time = ""

        day = userInfo["Day"][0]
        schedulesStr = schedulesArr[scheduleIndex]

        for schedule in schedulesStr.splitlines():
            activity, time = schedule.strip().split('->')
            newSchedules.append((activity, time))

        completeSchedule[day] = (schedulesStr)

        print(schedulesArr[scheduleIndex])
        print("HERE")
        print(newSchedules)

        # for year in range(self.calendarView.minimumDate().year(), self.calendarView.maximumDate().year() + 1):
        #     for month in range(1, 13):
        #         for day in range(1, 32):
        #             # Get the QDate object for the current day
        #             qdate = QDate(year, month, day)

        #             # Check if the day is a Monday
        #             if qdate.dayOfWeek() == Qt.DayOfWeek.Monday:
        #                 # Add information to the day using setToolTip
        #                 self.calendarView.setDateToolTip(qdate, schedulesStr.format(qdate.toString(Qt.DateFormat.ISODate)))

    def on_date_clicked(self):
        indexArr = list(completeSchedule.keys())
        daySelected = int(self.calendarView.selectedDate().dayOfWeek()) - 1
        print("heressss")
        print(completeSchedule[indexArr[daySelected]])
        print("here2")

        # self.descriptionTextBrowser.setText(completeSchedule[indexArr[daySelected]])

        self.scheduleListCal.clear()
        print(schedulesArr[scheduleIndex])

        if (completeSchedule[indexArr[daySelected]] != ""):
            tempArr = []
            for sched in completeSchedule[indexArr[daySelected]].splitlines():
                tempArr.append(sched)

            print(tempArr)
            self.scheduleListCal.addItems(tempArr)

    def indexChanged(self, current, previous):
        # Gets the index of the selected schedule

        print("textChanged")
        print(self.scheduleListCal.row(current))
        scheduleIndex = self.scheduleListCal.row(current)

        if (self.scheduleListCal.currentItem()):
            selectedRow = self.scheduleListCal.currentItem().text()
            print(f"YOYO {selectedRow}")

            activity = ""
            for tempEvent in selectedRow.splitlines():
                var1, var4 = tempEvent.strip().split('->')
                activity = var1

            print(activity)

            # activityIndex = userInfo["Activity"].index(activity)

            # print(userInfo["Description"][activityIndex])
            # self.descriptionTextBrowser.setText(userInfo["Description"][activityIndex])
            self.descriptionTextBrowser.setText(descriptionsGlob[activity])

        # print(self.calendarView.selectedDate().dayOfWeek()) #1 is Monday #7 is Sunday

    def go_to_page1(self):
        global userInfo
        global available_hours
        global tasks
        global scheduleIndex
        global schedulesArr
        global eventsAdded

        userInfo = {"Activity": [], "Description": [], "Hours": [], "Day": []}
        available_hours = {}
        tasks = {}
        schedulesArr = []
        scheduleIndex = 0
        eventsAdded = 0
        stacked_widget.setCurrentWidget(page1)


class SplashScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Spash Screen Example')
        self.setFixedSize(1280, 720)
        # self.setWindowFlag(Qt.FramelessWindowHint)
        # self.setAttribute(Qt.WA_TranslucentBackground)

        self.counter = 0
        self.n = 300  # total instance

        self.initUI()

        self.timer = QTimer()
        self.timer.timeout.connect(self.loading)
        self.timer.start(15)

    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.frame = QFrame()
        layout.addWidget(self.frame)

        self.progressBar = QProgressBar(self.frame)
        self.progressBar.resize(400, 30)
        self.progressBar.move(430, 620)
        self.progressBar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.progressBar.setFormat('%p%')
        self.progressBar.setTextVisible(True)
        self.progressBar.setRange(0, self.n)
        self.progressBar.setValue(20)

    def loading(self):
        self.progressBar.setValue(self.counter)

        if self.counter == int(self.n * 0.3):
            pass
        elif self.counter == int(self.n * 0.6):
            pass  # self.labelDescription.setText('<strong>Working on Task #3</strong>')
        elif self.counter >= self.n:
            self.timer.stop()
            self.close()

            time.sleep(1)

            stacked_widget.setCurrentWidget(page1)
            stacked_widget.setStyleSheet('''
                                        #MyWidget {
                                                background-color: #BFCCB5;
                                        }

                                        QFrame {
                                            background-color: #BFCCB5;
                                            background-image: url(background.png);
                                            background-repeat: no-repeat; 
                                            background-position: center;
                                            color: rgb(220, 220, 220);
                                        }

                                        QProgressBar {
                                            background-color: #1A1A1A;
                                            color: rgb(84, 84, 84);
                                            border-style: none;
                                            border-radius: 10px;
                                            text-align: center;
                                            font-size: 30px;
                                        }

                                        QProgressBar::chunk {
                                            border-radius: 10px;
                                            background-color: #FFFFFF;
                                        }
                                    ''')

        self.counter += 1


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.window_width, self.window_height = 1280, 720
        self.setMinimumSize(self.window_width, self.window_height)

        layout = QVBoxLayout()
        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # app.setStyleSheet('''
    #     QFrame {
    #         background-color: #2F4454;
    #         background-image: url(Splash.png);
    #         background-repeat: no-repeat;
    #         background-position: center;
    #         color: rgb(220, 220, 220);
    #     }

    #     QProgressBar {
    #         background-color: #1A1A1A;
    #         color: rgb(84, 84, 84);
    #         border-style: none;
    #         border-radius: 10px;
    #         text-align: center;
    #         font-size: 30px;
    #     }

    #     QProgressBar::chunk {
    #         border-radius: 10px;
    #         background-color: #FFFFFF;
    #     }
    # ''')

    # Create the pages
    splash = SplashScreen()
    page3 = Page3()
    page2 = Page2(page3)
    page1 = Page1(page2)

    # Create the stacked widget and add the pages to it
    stacked_widget = QStackedWidget()
    stacked_widget.addWidget(splash)
    stacked_widget.addWidget(page1)
    stacked_widget.addWidget(page2)
    stacked_widget.addWidget(page3)
    # stacked_widget.setCurrentWidget(page1)
    stacked_widget.setCurrentWidget(splash)

    stacked_widget.setGeometry(300, 300, 1280, 720)
    stacked_widget.setObjectName("MyWidget")
    stacked_widget.setStyleSheet('''
        #MyWidget {
                background-color: #BFCCB5;
        }

        QFrame {
            background-color: #2F4454;
            background-image: url(Splash.png);
            background-repeat: no-repeat; 
            background-position: center;
            color: rgb(220, 220, 220);
        }

        QProgressBar {
            background-color: #1A1A1A;
            color: rgb(84, 84, 84);
            border-style: none;
            border-radius: 10px;
            text-align: center;
            font-size: 30px;
        }

        QProgressBar::chunk {
            border-radius: 10px;
            background-color: #FFFFFF;
        }
    ''')

    # Show the stacked widget

    stacked_widget.show()

    sys.exit(app.exec())