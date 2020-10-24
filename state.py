from transitions import Machine
import common

class StateAction(Machine):
    def __init__(self):
        states = [ 
               'title',
               'menu',
               'photo', 
               'make',
               'puzzle',
               'result',
             ]
        Machine.__init__(self, states=states, initial='title')
        self.add_ordered_transitions()
        
    def on_enter_title(self):
        print('enter title')
        common.current_update = self.title_update
        common.current_input = self.title_input
        
        common.title_quad.enabled = True

    def title_update(self):
        print('update title')

    def title_input(self, key):
        print('input title, key:', key)
        if key == 'space':
            self.next_state()

    def on_exit_title(self):
        print('exit title')


    def on_enter_menu(self):
        print('enter menu')
        common.current_update = self.menu_update
        common.current_input = self.menu_input

    def menu_update(self):
        print('menu update')

    def menu_input(self, key):
        print('menu input')

    def on_exit_menu(self):
        print('exit menu ')


def init():
    machine = StateAction()
    common.state_machine = machine
    machine.to_title()
