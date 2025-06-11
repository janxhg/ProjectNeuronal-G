# test_matplotlib.py
print("Intentando importar matplotlib.pyplot...")
try:
    import matplotlib.pyplot as plt
    print("matplotlib.pyplot importado exitosamente.")
    # Opcional: intentar crear una figura simple
    # fig, ax = plt.subplots()
    # ax.plot([1, 2, 3], [1, 4, 9])
    # print("Figura simple creada.")
    # plt.show() # Esto podría fallar si el backend sigue siendo un problema
except Exception as e:
    print(f"ERROR al importar o usar matplotlib.pyplot: {e}")
    import traceback
    traceback.print_exc()
print("Fin del script de prueba.")