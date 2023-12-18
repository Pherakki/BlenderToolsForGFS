from .AnimationPropertiesPanelBase import generate_panel

OBJECT_PT_GFSToolsBaseAnimationPropsPanel = generate_panel(
    "BaseAnimation",
    "Base Animation",
    lambda context: context.object.data.GFSTOOLS_ModelProperties.get_selected_gap().get_selected_base_anim(),
    "test_anims",
    "test_anims_idx",
    ["active_anim_idx"]
)
