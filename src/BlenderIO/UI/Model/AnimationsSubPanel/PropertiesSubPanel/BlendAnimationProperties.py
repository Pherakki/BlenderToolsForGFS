from .AnimationPropertiesPanelBase import generate_panel

OBJECT_PT_GFSToolsBlendAnimationPropsPanel = generate_panel(
    "BlendAnimation",
    "GAP Blend Animations",
    lambda context: context.object.data.GFSTOOLS_ModelProperties.get_selected_gap().get_selected_blend_anim(),
    "test_blend_anims",
    "test_blend_anims_idx",
    []
)
