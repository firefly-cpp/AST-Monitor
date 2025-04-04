import sys,os,random
import pytest

try:
    from ast_monitor.model import AST
except ModuleNotFoundError:
    sys.path.append('../')
    from ast_monitor.model import AST
   


@pytest.fixture
def widget(qtbot):
    hr_data = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'sensor_data', 'hr.txt')
    gps_data = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'sensor_data', 'gps.txt')
    route_data = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'development', 'routes', 'route.json')
    random_port = random.randint(8000, 9000)    
    window = AST(hr_data, gps_data, route_data,server_port=random_port,logging=False)
    qtbot.addWidget(window)
    return window
    

def test_window_title(qtbot,widget):    
    assert widget.windowTitle() == "TrainingFeedback"
    widget.server_thread.stop()

def test_buttons(qtbot,widget):
    assert widget.btn_shutdown is not None
    assert widget.btn_start_tracking is not None
    assert widget.btn_stop_tracking is not None
    assert widget.btn_move_left is not None
    assert widget.btn_move_right is not None
    assert widget.btn_load_training is not None
    assert widget.btn_start_training is not None
    widget.server_thread.stop()

def test_menu_navigation(qtbot,widget):    
    assert widget.stackedWidget.count() == 4 # Currently has 4 pages
    assert widget.stackedWidget.currentIndex() == 2 # Start on Intervals, index should be 2
    widget.btn_move_left.click() # Map, index should now be 1
    assert widget.stackedWidget.currentIndex() == 1
    widget.btn_move_left.click() # Basic data, index should now be 0
    assert widget.stackedWidget.currentIndex() == 0
    widget.btn_move_right.click()
    widget.btn_move_right.click() # Intervals, index should now be 2
    assert widget.stackedWidget.currentIndex() == 2
    widget.btn_move_right.click() # Training, index should now be 3
    assert widget.stackedWidget.currentIndex() == 3
    widget.server_thread.stop()

def test_start_stop_tracking(qtbot,widget):
    assert widget.widget_start_stop.currentIndex() == 0 # Shows start icon, is stopped
    widget.btn_start_tracking.click()
    assert widget.widget_start_stop.currentIndex() == 1 # Shows stop icon, is running
    widget.btn_stop_tracking.click()
    assert widget.widget_start_stop.currentIndex() == 0 # Shows start icon, is stopped
    widget.server_thread.stop()

@pytest.mark.skip(reason="Skipping this test temporarily")
def test_load_training(qtbot,widget):    
    widget.btn_move_right.click() # Move to Training page
    widget.btn_load_training.click() # Load training
    assert widget.lbl_training_type.text() == "Interval"
    assert widget.lbl_training_speed_duration.text() == "1 min"
    assert widget.lbl_training_speed_hr.text() == "155"
    assert widget.lbl_training_rest_duration.text() == "1 min"
    assert widget.lbl_training_rest_hr.text() == "90"
    assert widget.lbl_training_repetitions.text() == "2"
    widget.server_thread.stop()
    
