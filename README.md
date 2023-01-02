# BlenderToolsForGFS
A Blender 2.83 plugin for importing and exporting GFS files.

⚠ **NOTE: THIS IS IS AN IN-DEVELOPMENT REPOSITORY. THIS PLUGIN IS NOT READY FOR ANY KIND OF PRODUCTION USE.** ⚠

<!--
#### ⚠ IMPORTANT NOTE ⚠

The export of models using this plugin is idiomatic and require a very specific arrangement of data and objects. Please [READ THE DOCUMENTATION]() (link incomplete for now, will link to documentation when written) to learn how to export models using the plugin.

You can also access the documentation from within Blender by inspecting the drop-down menu for the plugin in the Blender Preferences/Addons menu and clicking the link to the documentation, or by opening the PDF in the `docs` folder of the plugin repository.

#### ⚠ IMPORTANT NOTE ⚠
-->

## README Table of Contents
| Section | Contents |
|---|---|
| [Acknowledgements](#acknowledgements) | Important acknowledgements of assistance and resources used in the development of this library. |
| [Supported Formats](#supported-formats) | Formats supported by the plugin. |

## Acknowledgements
This is a Blender importer for the GFS file format. The research for this format was carried out by the following people, which directly enabled this plugin to be written:
- TGE
- PolarSoda
- mrdudesworkshop

Please make the repository owner aware if additional contributors are missing from this list.

Additionally, thanks to DniweTamp in the Persona Modding Community for helping me understand some aspects of the format.

## Supported Formats
The status of the code is tabulated for the different filetypes and versions given in the sections below, with the following keys:

| Key | Status | Definition |
| :---: | :---: | :--- |
|✔️| Supported | Import/export is production-ready .|
|🟡| Partial Support | An incomplete, but partially usable import/export operation exists.|
|❌| Not supported | Insufficient code exists for useful import/export. |

### GMD

| Version | Present In | Import | Export |
|:---:|:---:|:---:|:---:|
| 0x01105100 | Persona 5 Royal (PC) | ❌ | ❌ |
