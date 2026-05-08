# Compilar script Python con PyInstaller en Windows PowerShell

## Requisitos previos

- Python instalado (Microsoft Store o [python.org](https://www.python.org/downloads/))
- PowerShell abierto en la carpeta del proyecto

---

## Paso 1 — Instalar dependencias del script

Instala todos los módulos que usa tu script antes de compilar:

```powershell
pip install wmi
```

> Reemplaza `wmi` por los módulos que uses. Si tienes un `requirements.txt`:
> ```powershell
> pip install -r requirements.txt
> ```

---

## Paso 2 — Instalar PyInstaller

```powershell
pip install pyinstaller
```

---

## Paso 3 — Compilar el script

Usa `python -m PyInstaller` en lugar del comando directo `pyinstaller` para evitar problemas de PATH (especialmente con Python de Microsoft Store):

```powershell
python -m PyInstaller --onefile tu_script.py
```

### Flags útiles

| Flag | Efecto |
|------|--------|
| `--onefile` | Genera un único `.exe` autocontenido |
| `--noconsole` | Oculta la ventana de consola (apps GUI) |
| `--name=NombreApp` | Nombre del ejecutable de salida |
| `--icon=icono.ico` | Ícono personalizado |
| `--hidden-import=modulo` | Fuerza la inclusión de un módulo no detectado |

### Ejemplo completo

```powershell
python -m PyInstaller --onefile --hidden-import=wmi --name=mi_app tu_script.py
```

---

## Paso 4 — Ubicar el ejecutable

Una vez compilado, el `.exe` estará en:

```
dist/
  tu_script.exe   ← este es el archivo final
build/            ← archivos intermedios, puedes ignorar
tu_script.spec    ← configuración de la compilación
```

---

## Errores comunes

### `pyinstaller` no se reconoce
Usa siempre:
```powershell
python -m PyInstaller tu_script.py
```

### `Failed to load Python DLL '_internal\python313.dll'`
Ocurre cuando se copia solo el `.exe` sin la carpeta `_internal`. Solución: compilar con `--onefile` para evitar dependencias externas.

### `ModuleNotFoundError: No module named 'X'`
El módulo no fue detectado automáticamente. Instálalo y fuerza su inclusión:
```powershell
pip install X
python -m PyInstaller --onefile --hidden-import=X tu_script.py
```

### Error de Execution Policy
```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

---

## Referencia rápida

```powershell
# Instalar dependencias
pip install -r requirements.txt

# Compilar (comando recomendado)
python -m PyInstaller --onefile --hidden-import=wmi tu_script.py

# El exe final estará en:
# dist\tu_script.exe
```
