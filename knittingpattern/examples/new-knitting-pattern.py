import json

s = dict()

right_mesh = dict()
#    type of stitch
#    k means a knit stitch and p means a purl stitch. Thus, "k2, p2",
#      means "knit two stitches, purl two stitches". Similarly,
#      sl st describes a slip stitch, whereas yarn-overs are denoted with yo.
right_mesh["type"] = "knit"  # purl
#    scope of stitch
#    The modifier tog indicates that the stitches should be knitted together,
#      e.g., "k2tog" indicates that two stitches should be knitted together
#      as though they were one stitch. psso means "pass the slipped stitch
#      over". pnso means "pass the next stitch over".
right_mesh["scope"] = None
#    orientation of stitch
#    The modifier tbl indicates that stitches should be knitted
#      through the back loop. For example, "p2tog tbl" indicates
#      that two stitches should be purled together through the back toop.
#      kwise and pwise connote "knitwise" and "purlwise", usually referring
#      to a slip stitch.
right_mesh["orientation"] = 0  # degrees
#    insertion point of stitch
#    k-b and k1b mean "knit into the row below". Similarly, p-b and
#      p1b mean "purl into the row below".
#    p tbl; P1 tbl; or P1b: Purl through the back loop.
right_mesh["insertion_point"] = None

MESHES_IN_ROW_1 = 5
MESHES_IN_ROW_2 = 7

row1 = dict()
row1["meshes"] = [right_mesh] * MESHES_IN_ROW_1
#   side of work
#   RS and WS signify the "right side" and "wrong side" of the work.
row1["side"] = "right"  # wrong
row1["id"] = "row1"

s["type"] = "knitting pattern"
s["version"] = "0.1"
s["rows"] = [row1]
s["row_connections"] = [{"from": {"id": "row1",
                                  "first": 1,
                                  "last": MESHES_IN_ROW_1},
                         "to": {"id": "row2",
                                "first": 1,
                                "last": MESHES_IN_ROW_2}}]

print(json.dumps(s, indent=2))
