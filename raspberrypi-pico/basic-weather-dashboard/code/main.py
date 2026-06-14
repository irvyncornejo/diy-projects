from applications import Applications


if __name__=='__main__':

    try:
        
        app = Applications()
        
        while True:
            app.run()

    except Exception as e:
            print(e)
