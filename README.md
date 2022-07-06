# Demo for Problem with Calc Addin development in Windows vs Linux
1. Install [LibreOffice/CoolProp.oxt](LibreOffice/CoolProp.oxt) into Libreoffice
2. Restart Libreoffice
3. Launch Libreoffice Calc
4. Goto Tools->Options->CoolProp->Install Python Package. Ensure it displays "Successfully installed Python Package"
5. Restart Libreoffice and launch calc with [wrappers/LibreOffice/Test.ods](wrappers/LibreOffice/Test.ods)
6. It is expected to have the following in the first 2 cells:

    <class 'float'>
    
    <class 'str'>

## Steps to build from source:
Execute from project root directory:
```
cmake -DCOOLPROP_LIBREOFFICE_MODULE=ON -DLO_PROGRAM_PATH=/usr/lib/libreoffice/program -DLO_SDK_PATH=/usr/lib/libreoffice/sdk && make CoolPropLibreOfficeAddin
```

## Acknowledgement
This example was created from source code forked from [https://github.com/CoolProp/CoolProp/](https://github.com/CoolProp/CoolProp/)