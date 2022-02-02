# Py module ot create collection for renderlayer

import maya.cmds as cmds
import maya.api.OpenMaya as OpenMaya


def shaderCheck(shader_name):
    check = cmds.objExists("%s" % shader_name)
    return check


def createShader(name, r, g, b, node_type="RedshiftIncandescent"):
    if not shaderCheck(name):
        material = cmds.shadingNode(node_type, name=name, asShader=True)
        sg = cmds.sets(name="%s_sg" % name, empty=True, renderable=True, noSurfaceShader=True)
        cmds.connectAttr("%s.outColor" % material, "%s.surfaceShader" % sg)
        sg = cmds.sets(name="%s_sg" % name, empty=True, renderable=True, noSurfaceShader=True)
        cmds.setAttr("%s.color" % name, r, g, b, type="double3")
        return material, sg
    else:
        print("[ShaderCheck]")
        print("[ShaderCheck] %s already created" % name)
        print("[ShaderCheck]")


def renderLayerCheck(layer_type, render_layer):
    check = cmds.objExists('{layer_type}_{render_layer}'.format(layer_type=layer_type, render_layer=render_layer))
    return check


def collectionCheck(layer_type, layer_descript, aov):
    check = cmds.objExists(
        '{layer_type}_{layer_descript}_{aov}'.format(layer_type=layer_type, layer_descript=layer_descript, aov=aov))
    return check


def selPattern(list):
    sel = ",".join(list)
    for item in list:
        print("[Selection Pattern] %s" % item)
    return sel


def aovOverride(render_layer, layer_descript, layer_type, aov, sel_pattern):
    c17 = render_layer.createCollection('{layer_type}_{layer_descript}_AOV_col'.format(layer_type=layer_type,

                                                                                       layer_descript=layer_descript))
    c17.getSelector().setPattern(sel_pattern)
    cmds.setAttr(c17.name() + 'Selector.typeFilter', 8)
    c17.getSelector().setCustomFilterValue('RedshiftAOV')

    cmds.setAttr(c17.name() + "Selector.staticSelection", aov, type="string")
    ov1 = c17.createAbsoluteOverride(aov, 'enabled')
    ov1.setAttrValue(False)


def displacementOverride(render_layer, layer_descript, layer_type, sel_pattern):
    c18 = render_layer.createCollection('{layer_type}_{layer_descript}_disp_col'.format(layer_type=layer_type,
                                                                                       layer_descript=layer_descript))
    c18.getSelector().setPattern(sel_pattern)
    c19 = c18.createCollection('{layer_type}_{layer_descript}_disp_shapes_col'.format(layer_type=layer_type,
                                                                                      layer_descript=layer_descript))
    cmds.setAttr(c19.name() + 'Selector.typeFilter', 2)
    c19.getSelector().setPattern('*')

    or9 = c19.createOverride('{layer_type}_{layer_descript}_disp_or'.format(layer_type=layer_type,
                                                                            layer_descript=layer_descript),
                             OpenMaya.MTypeId(0x58000378))
    or9.setAttributeName("rsEnableDisplacement")
    or9.finalize("rsEnableDisplacement")
    cmds.setAttr(or9.name() + ".attrValue", 0)


def tessOverride(render_layer, layer_descript, layer_type, sel_pattern):
    c18 = render_layer.createCollection('{layer_type}_{layer_descript}_tess_col'.format(layer_type=layer_type,
                                                                                       layer_descript=layer_descript))
    c18.getSelector().setPattern(sel_pattern)
    c19 = c18.createCollection('{layer_type}_{layer_descript}_tess_shapes_col'.format(layer_type=layer_type,
                                                                                      layer_descript=layer_descript))
    cmds.setAttr(c19.name() + 'Selector.typeFilter', 2)
    c19.getSelector().setPattern('*')

    or9 = c19.createOverride('{layer_type}_{layer_descript}_tess_or'.format(layer_type=layer_type,
                                                                            layer_descript=layer_descript),
                             OpenMaya.MTypeId(0x58000378))
    or9.setAttributeName("rsEnableSubdivision")
    or9.finalize("rsEnableSubdivision")
    cmds.setAttr(or9.name() + ".attrValue", 0)


def cryptoCol(render_layer, layer_type, layer_descript):
    cryptoAOVs = []
    sceneAOVs = cmds.ls(type="RedshiftAOV")
    cryptoCheck = False

    for sceneAOV in sceneAOVs:
        getAovtype = cmds.getAttr(sceneAOV + ".aovType")
        # print(getAovtype)
        if getAovtype == "Cryptomatte":
            # print("Cryptomatte exists")
            cryptoAOVs.append(sceneAOV)
            cryptoCheck = True
        else:
            continue

    cryptoAOVslist = " ".join(cryptoAOVs)
    print(cryptoAOVslist)

    if cryptoCheck:
        c102 = render_layer.createCollection('{layer_type}_{layer_descript}_crypto_off'.format(layer_type=layer_type,
                                                                                               layer_descript=
                                                                                               layer_descript))
        cmds.setAttr(c102.name() + 'Selector.typeFilter', 8)
        c102.getSelector().setCustomFilterValue('RedshiftAOV')
        cmds.setAttr(c102.name() + "Selector.staticSelection", cryptoAOVslist, type="string")
        or102 = c102.createOverride('{layer_type}_{layer_descript}_crypto_off'.format(layer_type=layer_type,
                                                                                      layer_descript=layer_descript),
                                    OpenMaya.MTypeId(0x58000378))
        or102.setAttributeName("enabled")
        or102.finalize("enabled")
        cmds.setAttr(or102.name() + ".attrValue", 0)
        cmds.setAttr(c102.name() + '.selfEnabled', 1)


def shdwCatcherCol(render_layer, layer_descript, layer_type, sel_pattern):
    c9 = render_layer.createCollection('{layer_type}_{layer_descript}_shdw_catcher_col'.format(layer_type=layer_type,
                                                                                              layer_descript=layer_descript))
    c9.getSelector().setPattern(sel_pattern)
    c10 = c9.createCollection('{layer_type}_{layer_descript}_shapes_col'.format(layer_type=layer_type,
                                                                                layer_descript=layer_descript))
    cmds.setAttr(c10.name() + 'Selector.typeFilter', 2)
    c10.getSelector().setPattern('*')
    ov5_1 = c10.createOverride('{layer_type}_{layer_descript}_shdw_matte_or'.format(layer_type=layer_type,
                                                                                    layer_descript=layer_descript),
                               OpenMaya.MTypeId(0x58000378))
    ov5_1.setAttributeName("rsMatteEnable")
    ov5_1.finalize("rsMatteEnable")
    cmds.setAttr(ov5_1.name() + ".attrValue", 1)
    ov5_2 = c10.createOverride('{layer_type}_{layer_descript}_shdw_enable_or'.format(layer_type=layer_type,
                                                                                     layer_descript=layer_descript),
                               OpenMaya.MTypeId(0x58000378))
    ov5_2.setAttributeName("rsMatteShadowEnable")
    ov5_2.finalize("rsMatteShadowEnable")
    cmds.setAttr(ov5_2.name() + ".attrValue", 1)
    ov5_3 = c10.createOverride('{layer_type}_{layer_descript}_shdw_receive_or'.format(layer_type=layer_type,
                                                                                      layer_descript=layer_descript),
                               OpenMaya.MTypeId(0x58000378))
    ov5_3.setAttributeName("rsMatteReceiveShadowsFromMattes")
    ov5_3.finalize("rsMatteReceiveShadowsFromMattes")
    cmds.setAttr(ov5_3.name() + ".attrValue", 0)
    ov5_4 = c10.createOverride('{layer_type}_{layer_descript}_shdw_alpha_or'.format(layer_type=layer_type,
                                                                                    layer_descript=layer_descript),
                               OpenMaya.MTypeId(0x58000378))
    ov5_4.setAttributeName("rsMatteShadowAffectsAlpha")
    ov5_4.finalize("rsMatteShadowAffectsAlpha")
    cmds.setAttr(ov5_4.name() + ".attrValue", 1)


def visOffCol(render_layer, layer_descript, layer_type, sel_pattern):
    c8 = render_layer.createCollection('{layer_type}_{layer_descript}_vis_off_col'.format(layer_type=layer_type,
                                                                                         layer_descript=layer_descript))
    c8.getSelector().setPattern(sel_pattern)

    ov4 = c8.createOverride('{layer_type}_{layer_descript}_vis_off'.format(layer_type=layer_type,
                                                                           layer_descript=layer_descript),
                            OpenMaya.MTypeId(0x58000378))
    ov4.setAttributeName("visibility")
    ov4.finalize("visibility")
    cmds.setAttr(ov4.name() + ".attrValue", 0)


def visOnCol(render_layer, layer_descript, layer_type,  sel_pattern):
    c7 = render_layer.createCollection('{layer_type}_{layer_descript}_vis_on_col'.format(layer_type=layer_type,
                                                                                         layer_descript=layer_descript))
    c7.getSelector().setPattern(sel_pattern)
    ov3 = c7.createOverride('{layer_type}_{layer_descript}_vis_on'.format(layer_type=layer_type,
                                                                          layer_descript=layer_descript),
                            OpenMaya.MTypeId(0x58000378))
    ov3.setAttributeName("visibility")
    ov3.finalize("visibility")
    cmds.setAttr(ov3.name() + ".attrValue", 1)


def primeVisOffCol(render_layer, layer_descript, layer_type, sel_pattern):
    c5 = render_layer.createCollection('{layer_type}_{layer_descript}_primvis_off_col'.format(layer_type=layer_type,
                                                                                              layer_descript=layer_descript))
    c5.getSelector().setPattern('{sel_pattern}'.format(sel_pattern=sel_pattern))
    c6 = c5.createCollection('{layer_type}_{layer_descript}_primvis_shapes_col'.format(layer_type=layer_type,
                                                                                       layer_descript=layer_descript))
    cmds.setAttr(c6.name() + 'Selector.typeFilter', 2)
    c6.getSelector().setPattern('*')
    #   MoonKnight Prime Vis Override
    ov2 = c6.createOverride('{layer_type}_{layer_descript}_primaryVis_or'.format(layer_type=layer_type,
                                                                                 layer_descript=layer_descript),
                            OpenMaya.MTypeId(0x58000378))
    ov2.setAttributeName("primaryVisibility")
    ov2.finalize("primaryVisibility")
    cmds.setAttr(ov2.name() + ".attrValue", 0)


def holdoutCol(render_layer, layer_descript, layer_type, sel_pattern):
    c3 = render_layer.createCollection('{layer_type}_{layer_descript}_holdout_col'.format(layer_type=layer_type,
                                                                                          layer_descript=layer_descript))
    c3.getSelector().setPattern(sel_pattern)

    c4 = c3.createCollection('{layer_type}_{layer_descript}_shapes_col'.format(layer_type=layer_type,
                                                                               layer_descript=layer_descript))
    cmds.setAttr(c4.name() + 'Selector.typeFilter', 2)
    c4.getSelector().setPattern('*')
    ov1_1 = c4.createOverride("{layer_type}_{layer_descript}_holdout_matte_or".format(layer_type=layer_type,
                                                                                      layer_descript=layer_descript),
                              OpenMaya.MTypeId(0x58000378))
    ov1_1.setAttributeName("rsMatteEnable")
    ov1_1.finalize("rsMatteEnable")
    cmds.setAttr(ov1_1.name() + ".attrValue", 1)
    ov1_2 = c4.createOverride('{layer_type}_{layer_descript}_holdout_alpha_or'.format(layer_type=layer_type,
                                                                                      layer_descript=layer_descript),
                              OpenMaya.MTypeId(0x58000378))
    ov1_2.setAttributeName("rsMatteAlpha")
    ov1_2.finalize("rsMatteAlpha")
    cmds.setAttr(ov1_2.name() + ".attrValue", 0)


def shapesCol(render_layer, layer_descript, layer_type, sel_pattern):
    c1 = render_layer.createCollection('{layer_type}_{layer_descript}_col'.format(layer_type=layer_type,
                                                                                  layer_descript=layer_descript))
    c1.getSelector().setPattern(sel_pattern)
    c2 = c1.createCollection('{layer_type}_{layer_descript}_shapes_col'.format(layer_type=layer_type,
                                                                               layer_descript=layer_descript))
    cmds.setAttr(c2.name() + 'Selector.typeFilter', 2)
    c2.getSelector().setPattern('*')


def rs_colorToAov_col(render_layer, selection_pattern, layer_descript, layer_type, name, shader):
    c13 = render_layer.createCollection('{layer_type}_{layer_descript}_{name}_col'.format(layer_type=layer_type,
                                                                                          layer_descript=layer_descript,
                                                                                          name=name))
    cmds.setAttr(c13.name() + 'Selector.typeFilter', 8)
    c13.getSelector().setCustomFilterValue('RedshiftStoreColorToAOV')
    c13.getSelector().setPattern(selection_pattern)

    ov7 = c13.createOverride('{layer_type}_{layer_descript}_{name}_col'.format(layer_type=layer_type,
                                                                               layer_descript=layer_descript,
                                                                               name=name),
                             OpenMaya.MTypeId(0x58000385))
    ov7.setAttributeName("beauty_input")
    ov7.finalize("beauty_input")
    cmds.connectAttr("{shader}.outColor".format(shader=shader), "{name}.attrValue".format(name=ov7.name()))


def rs_colorToAovGeo_col(layer_descript, layer_type, render_layer, sel_pattern):
    c15 = render_layer.createCollection('{layer_type}_{layer_descript}_geo_msk_col'.format(layer_type=layer_type,
                                                                                           layer_descript=layer_descript))
    cmds.setAttr(c15.name() + 'Selector.typeFilter', 1)
    c15.getSelector().setPattern(sel_pattern)


def matOverride_col(render_layer, selection_pattern, layer_descript, layer_type,  name, shader):
    c16 = render_layer.createCollection('{layer_type}_{layer_descript}_{name}_col'.format(layer_type=layer_type,
                                                                                          layer_descript=layer_descript,
                                                                                          name=name))
    c16.getSelector().setPattern(selection_pattern)

    ov9 = c16.createOverride(('{layer_type}_{layer_descript}_{name}_msk'.format(layer_type=layer_type,
                                                                                layer_descript=layer_descript,
                                                                                name=name)), "shaderOverride")
    # assign shader
    ov9.setShader("{shader}".format(shader=shader))
