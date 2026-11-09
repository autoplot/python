# Testing Autoplot for Python

This guide describes how to verify that the Python Autoplot package installs and operates correctly on Linux, macOS, and Windows.

Autoplot uses JPype to access Java, so Python, JPype, and the Java Virtual Machine (JVM) must be compatible.

## 1. Create a clean Python environment

Use a fresh virtual environment to avoid interference from previously installed packages.

On Linux or macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install --no-cache-dir autoplot
```

On Windows, activate with `.venv\Scripts\activate` instead.

Verify the installed package:

```bash
python -m pip show autoplot JPype1
```

The reported Autoplot version should match the intended PyPI release.

## 2. Verify the platform

Run:

```python
import sys
import platform
import jpype

print("Python:", sys.version)
print("Python executable:", sys.executable)
print("Operating system:", platform.platform())
print("Architecture:", platform.machine())
print("JPype:", jpype.__version__)
print("JVM library:", jpype.getDefaultJVMPath())
```

Also check Java from the terminal:

```bash
java -version
```

**Important:** Python and the JVM loaded by JPype must have compatible CPU architectures.

On macOS, especially Apple Silicon, check the actual JVM library:

```bash
file /path/to/libjvm.dylib
lipo -archs /path/to/libjvm.dylib
```

The `java` command on your PATH is not necessarily the JVM that JPype will load.

## 3. Test JPype independently

Before testing Autoplot, verify that JPype can start Java.

Run this in a fresh Python process:

```python
import jpype

print("JVM:", jpype.getDefaultJVMPath(), flush=True)

jpype.startJVM()

print("Started:", jpype.isJVMStarted(), flush=True)
print("Java version:",
      jpype.java.lang.System.getProperty("java.version"))
print("Java architecture:",
      jpype.java.lang.System.getProperty("os.arch"))

jpype.shutdownJVM()
```

Expected result: the JVM starts, prints its version and architecture, and exits normally.

If Python crashes or segfaults here, the problem is independent of Autoplot. Investigate JPype compatibility, JVM architecture, and Java installation before proceeding.

Avoid enabling Python's `faulthandler` for the initial test because it may interfere with the JVM's signal handling.

## 4. Test Autoplot initialization

In a new Python process:

```python
import jpype
import autoplot as ap

ap.init()

assert jpype.isJVMStarted()
print("Autoplot initialized successfully")
```

This tests Autoplot's initialization, including locating its Java libraries and starting the JVM.

The first run may download `autoplot.jar`.

## 5. Test data access

Once initialization works, test loading a dataset and converting it to NumPy arrays.

```python
import autoplot as ap

ap.init()

ds = ap.APDataSet()
ds.setDataSetURI(
    "https://autoplot.org/data/swe-np.xls"
    "?column=data&depend0=dep0"
)

ds.doGetDataSet()

print(ds.toString())

values = ap.to_ndarray(ds, "data")
times = ap.to_ndarray(ds, "dep0")

assert len(values) > 0
assert len(values) == len(times)

print("Autoplot data access successful")
```

This checks Java integration, data loading, and NumPy conversion. It requires network access to the sample data source.

## 6. Diagnosing failures

| Symptom | Likely cause |
|---|---|
| `JVM DLL not found` | JVM not found or incompatible architecture |
| Segmentation fault in `startJVM()` | JPype/JVM native compatibility problem |
| `ClassNotFoundException` | Missing or incorrect Java classpath |
| Failure during `ap.init()` | Autoplot initialization or JAR download problem |
| Failure during `doGetDataSet()` | Data source, network, or Java reader problem |
| Failure during `to_ndarray()` | JPype/NumPy conversion problem |

When reporting an issue, include:

- Operating system and CPU architecture
- Python version and executable path
- JPype version
- Java version and JVM library path
- Autoplot package version
- Full error message and the step that failed

## 7. Recommended release verification

For every PyPI release, test on a clean environment using the published package rather than a local source checkout.

Recommended platforms:

- Linux x86_64
- macOS ARM64 (Apple Silicon)
- macOS x86_64, if supported
- Windows x86_64

Run the tests in order: installation, platform inspection, JPype startup, Autoplot initialization, and data access.

**Do not proceed to Autoplot tests if the standalone JPype test crashes.** This isolates JVM compatibility problems from defects in Autoplot itself.
