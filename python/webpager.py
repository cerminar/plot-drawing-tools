import os
import shutil

def confirm():
    yesAnswers = ['yes', 'y'];
    noAnswers = ['no', 'n']
    
    answer = input('Yes/No: ').lower().strip()

    if answer in yesAnswers:
        return True
    elif answer in noAnswers:
        return False
    else:
        return confirm()


class WebPageCreator(object):
    def __init__(self, top_dir, base_path='~/CERNbox/www/plots') -> None:
        self.base_path = base_path
        self.top_dir = top_dir
        self.canvases = {}

    def add(self, name, canvas):
        if name in self.canvases.keys():
            print(f'[WebPageCreator]***Warning: overwriting canvas: {name}!')
        self.canvases[name] = canvas

    def publish(self, directory):
        top_path = os.path.join(self.base_path, self.top_dir)
        target_dir = os.path.join(top_path, directory)
        
        if not os.path.exists(top_path):
            os.mkdir(top_path)
            shutil.copyfile(os.path.join(self.base_path, 'index.php'), os.path.join(top_path, 'index.php'))
            
        if os.path.exists(target_dir):
            print(f'WARNING: directory: {target_dir} already exists. Content might be overwritten?')
            if not confirm():
                return
        else:
            os.mkdir(target_dir)
            shutil.copyfile(os.path.join(self.base_path, 'index.php'), os.path.join(target_dir, 'index.php'))

        for name,canvas in self.canvases.items():
            print(f'publishing canvas: {name}')
            for ext in ['png', 'pdf']:
                canvas.SaveAs(os.path.join(target_dir, f'{name}.{ext}'))
        return


    
