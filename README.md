# BlenderToolsForGFS
A Blender 2.81+ plugin for importing and exporting GFS and GAP files.

A collection of preset materials, which you should use alongside this plugin to maximise your likelihood of a successful export, can be found in MadMax1960's [GFD Asset Library](https://github.com/MadMax1960/gfd-asset-library) repository.

<!--
#### ⚠ IMPORTANT NOTE ⚠

The export of models using this plugin is idiomatic and require a very specific arrangement of data and objects. Please [READ THE DOCUMENTATION]() (link incomplete for now, will link to documentation when written) to learn how to export models using the plugin.

You can also access the documentation from within Blender by inspecting the drop-down menu for the plugin in the Blender Preferences/Addons menu and clicking the link to the documentation, or by opening the PDF in the `docs` folder of the plugin repository.

#### ⚠ IMPORTANT NOTE ⚠
-->

## README Table of Contents
| Section | Contents |
|---|---|
| [Plugin Installation](#plugin-installation) | Important notes on plugin installation beyond regular addon registry. |
| [Plugin Usage](#plugin-usage) | Important notes on using the plugin. |
| [Limitations](#limitations) | Plugin limitations. |
| [Future Development](#future-development) | Notes on the most important features that are missing from the plugin. |
| [Acknowledgements](#acknowledgements) | Important acknowledgements of assistance and resources used in the development of this library. |
| [Supported Formats](#supported-formats) | Formats supported by the plugin. |

## Plugin Installation
The plugin comes bundled with documentation. In the source repository, this is just a LaTeX file plus the required images to build it, and the buttons in the Blender UI designed to open it will fail if you just install the addon from the develop branch. Therefore you have two options for install:
- Install the latest release.
- Download the code, and either:
    - Build the LaTeX file from source (out of scope for this README).
    - Unzip the addon, take the `Documentation.pdf` from the latest release, put in the `docs` folder of the downloaded code, zip the addon back up and install it.

## Plugin Usage
BlenderToolsForGFS makes a few idiomatic choices, such as, but not limited to:
- UV maps must be named UV0 through to UV7, in order to preserve texture coordinate animations.
- Imported meshes can be parented under other meshes to represent the fact that they share a node transform.
- Cameras and Lights are attached to bones using `ChildOf` constraints.
- Blend Animations must be split into two Actions - one for Translations and Rotations, and one for Scales.

**You should read the documentation if you need to understand the idiomatic choices used to export data. You can use imported files as a reference to see how data is imported.** There are many opportunites to open the documentation from within Blender by clicking the `How to Use` buttons on many of the data properties panels added by the plugin.

All data from the GFS or GAP file should be preserved from import to export, but not all of it will be represented in Blender. Most of the this data is stored as raw byte data on hidden properties inaccessible to the user. Use dedicated software such as [GFD Studio](https://github.com/tge-was-taken/GFD-Studio) to edit data the plugin is not capable of making accessible to the user.

## Limitations
- Camera aspect ratios are not displayed in Blender.
- Most aspects of Lights are not displayed in Blender.
- Materials are only implemented as using the Diffuse Texture. All Material data is imported, but most is not rendered in order to not be misleading.
- Physics data is not displayed.
- EPL data is not displayed.
- All animations other than Node/Bone animations are not displayed.

## Known Bugs
- Names not decodable as UTF-8 will cause import errors. Since all vanilla models use UTF-8, this bug can only be triggered by edited files.
- Meshes rigged or attached to the root bone will import and export incorrectly.
- The following vanilla P5R models will fail to re-export:
    - MODEL/CHARACTER/0006/C0006_103_00.GMD
    - MODEL/CHARACTER/5905/C5905_001_00.GMD
    - MODEL/FIELD_TEX/OBJECT/M051_040.GMD
    - MODEL/FIELD_TEX/OBJECT/M062_078.GMD
    - MODEL/FIELD_TEX/OBJECT/M062_080.GMD
    - MODEL/FIELD_TEX/OBJECT/M062_081.GMD

## Future Development
The highest-priority features are, in order of importance:
1) A custom Material Node that faithfully reproduces the material rendering.
2) Ability to import, manipulate, and export multiple animations packs simultaneously.
3) Ability to link multiple Blender Actions together into a single GFS animation.
4) Ability to activate and deactivate "combined" Actions from a UI panel.
5) Import and editability of material, camera, and morph animations (requires all prior features to be implemented first).
6) Import, manipulation, and export of physics colliders.
7) Import, manipulation, and export of submodels in EPL data.
8) Import, manupulation, and export of the model data in EPL files.

## Acknowledgements
This is a Blender importer for the GFS file format. The GFS format code has been heavily derived from [GFD Studio](https://github.com/tge-was-taken/GFD-Studio), tge's [3DS Max importer](https://github.com/tge-was-taken/GFD-Studio/tree/master/Resources/GfdImporter), and the [010 Editor templates](https://github.com/CherryCreamSoda/010-Editor-Templates/blob/master/templates/p5_gfd.bt). Deep thanks are given to all those who have contributed to the understanding of the format.

Additionally, thanks to CherryCreamSoda, DeathChaos, DniweTamp, A Mudkip, ShrineFox, and tge for providing feedback on the plugin development and for assisting with the comprehension of aspects of the GFS file format.

## Supported Formats
The status of the code is tabulated for the different filetypes and versions given in the sections below, with the following keys:

| Key | Status | Definition |
| :---: | :---: | :--- |
|✔️| Supported | Import/export is production-ready .|
|🟡| Partial Support | An incomplete, but partially usable import/export operation exists.|
|❌| Not supported | Insufficient code exists for useful import/export. |

### GMD

| Version | Present In | Import | Export | Notes |
|:---:|:---:|:---:|:---:|:---:|
| 0x01104920 - 0x01105100 | Persona 5 Royal (PC) | 🟡 | 🟡 | (1) |

(1) There are several missing features, noted in [Future Development](#future-development), that would be necessary for full GFS support.
