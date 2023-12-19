from .AnimationPropertiesPanelBase import generate_panel


OBJECT_PT_GFSToolsLookAtAnimationPropsPanel = generate_panel(
    "LookAtAnimation",
    "GAP LookAt Animations",
    lambda context: context.object.data.GFSTOOLS_ModelProperties.get_selected_gap().get_selected_lookat_anim(),
    "test_lookat_anims",
    "test_lookat_anims_idx",
    []
)
