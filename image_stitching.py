from msilib.schema import Error
import cv2, glob
import imutils

#directory in which all images are present
directory =  "C:\Study\\adsys\stitching\images\Overlapping_Microscope-1_set5\*"

images = [cv2.imread(frame) for frame in glob.glob(directory)]


parent = [i for i in range(len(images))]

def find(i):
    if parent[i] != i:
        parent[i] = find(parent[i])
    return parent[i]

stitcher = cv2.createStitcher() if imutils.is_cv3() else cv2.Stitcher_create()

for i in range(len(images)-1):
    for j in range(i+1, len(images)):
        try:
            (status, stitched) = stitcher.stitch([images[i], images[j]])
            if status == 0:
                p = find(i)
                q = find(j)

                if p != q:
                    parent[p] = q
                    
        except cv2.error:
            pass

disjoint_set = [find(i) for i in range(len(parent))]

disjoint = dict()

for i in range(len(disjoint_set)):
    if disjoint_set[i] not in disjoint:
        disjoint[disjoint_set[i]] = [i]
    else:
        disjoint[disjoint_set[i]].append(i)

for key in disjoint:
    (status, disjoint[key]) = stitcher.stitch([images[i] for i in disjoint[key]])
    if status == 0:
        cv2.imwrite(str(key)+".png", disjoint[key])
        # cv2.imshow(str(key), disjoint[key])
        # cv2.waitKey(0)
