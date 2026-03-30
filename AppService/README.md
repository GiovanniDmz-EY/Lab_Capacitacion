# Aplicación Flask Básica

Esta es una aplicación básica en Flask que muestra una página de inicio con el mensaje "Bienvenido" y el valor de la variable de entorno `mi_entorno`.

## Instalación

1. Instala las dependencias:
   
   ```bash
   pip install -r requirements.txt
   ```

2. Ejecuta la aplicación:
   
   ```bash
   python app/app.py
   ```

## Variable de entorno

Puedes definir la variable de entorno `mi_entorno` antes de ejecutar la app:

- En Windows (CMD):
  ```cmd
  set mi_entorno=valor
  python app/app.py
  ```
- En PowerShell:
  ```powershell
  $env:mi_entorno="valor"
  python app/app.py
  ```

Si la variable no está definida, mostrará "No definido".
