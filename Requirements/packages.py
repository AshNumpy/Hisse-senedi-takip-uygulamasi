import pip 

libraries = ["Pandas", "Numpy", "prophet", "streamlit", "plotly", "matplotlib"]

for lib in libraries:
    try:
        __import__(lib) 
        print(f'{lib} already up to date.')
    except:
        pip.main(['install',lib])
        print(f'{lib} installed.')