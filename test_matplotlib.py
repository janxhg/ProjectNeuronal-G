import matplotlib
matplotlib.use('Agg')
print('--- Matplotlib Test ---')
print('Attempting to import matplotlib.pyplot...')
try:
    import matplotlib.pyplot as plt
    print('Import successful!')
except Exception as e:
    print(f'An error occurred: {e}')
print('--- Test Finished ---')
