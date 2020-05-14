import os
import cv2
import numpy as np
import tensorflow as tf
from utils import label_map_util
import scipy.spatial.distance as dist
from utils import visualization_utils as vis_util
from utils import visualization_utils_new_tumor as vis_new_tum
###########################################
def Tumor_Detection(Brain_Image):
    MODEL_NAME = 'inference_graph'
    CWD_PATH = os.getcwd()
    PATH_TO_CKPT = os.path.join(CWD_PATH,MODEL_NAME,'frozen_inference_graph.pb')
    PATH_TO_LABELS = os.path.join(CWD_PATH,'training','labelmap.pbtxt')
    NUM_CLASSES = 5
    label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
    categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
    category_index = label_map_util.create_category_index(categories)
    detection_graph = tf.Graph()
    with detection_graph.as_default():
        od_graph_def = tf.GraphDef()
        with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')
        sess = tf.Session(graph=detection_graph)

    image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
    detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
    detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
    detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
    num_detections = detection_graph.get_tensor_by_name('num_detections:0')
    image = (Brain_Image)
    image_expanded = np.expand_dims(image, axis=0)
    (boxes, scores, classes, num) = sess.run(
        [detection_boxes, detection_scores, detection_classes, num_detections],
        feed_dict={image_tensor: image_expanded})
    vis_util.set_found(False)
    vis_util.visualize_boxes_and_labels_on_image_array(
        image,
        np.squeeze(boxes),
        np.squeeze(classes).astype(np.int32),
        np.squeeze(scores),
        category_index,
        use_normalized_coordinates=True,
        line_thickness=8,
        min_score_thresh=0.50)
    return vis_util.found,image
def Detection_Tumor(BRAIN_IMAGE):
    MODEL_NAME = 'inference_graph'
    CWD_PATH = os.getcwd()
    PATH_TO_CKPT = os.path.join(CWD_PATH, MODEL_NAME, 'frozen_inference_graph.pb')
    PATH_TO_LABELS = os.path.join(CWD_PATH, 'training', 'labelmap.pbtxt')
    NUM_CLASSES = 5
    label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
    categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES,
                                       use_display_name=True)
    category_index = label_map_util.create_category_index(categories)
    detection_graph = tf.Graph()
    with detection_graph.as_default():
        od_graph_def = tf.GraphDef()
        with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')
        sess = tf.Session(graph=detection_graph)
    image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
    detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
    detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
    detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
    num_detections = detection_graph.get_tensor_by_name('num_detections:0')
    image = (BRAIN_IMAGE)
    image_expanded = np.expand_dims(image, axis=0)
    (boxes, scores, classes, num) = sess.run(
        [detection_boxes, detection_scores, detection_classes, num_detections],
        feed_dict={image_tensor: image_expanded})
    vis_new_tum.set_found(False)
    vis_new_tum.visualize_boxes_and_labels_on_image_array(
        image,
        np.squeeze(boxes),
        np.squeeze(classes).astype(np.int32),
        np.squeeze(scores),
        category_index,
        use_normalized_coordinates=True,
        line_thickness=8,
        min_score_thresh=0.50)
    return vis_new_tum.found,image,vis_new_tum.Tumor_Name_List

Folder='IMAGES'
path=os.listdir(Folder)
count=1
counter_break=0
##########################################################################################
for Image in path:
    new=cv2.imread(os.path.join(Folder,Image))
    counter_break=counter_break+1
    Read_Image=new.copy()
    Tumor_Image=new.copy()
    Bool,TUMOR_IMAGE,name_list=Detection_Tumor(new)
    if Bool == False:
        font = cv2.FONT_HERSHEY_SIMPLEX
        org = (50, 50)
        fontScale = 1
        color = (102,205,0)
        thickness = 2
        cv2.putText(TUMOR_IMAGE, 'Tumor not found', org, font,
                    fontScale, color, thickness, cv2.LINE_AA)
        cv2.imwrite(("Detection_Images/"+Image),TUMOR_IMAGE)
    elif Bool == True:
        print("hello world")
        print("working on braintd ")
        print("Name",name_list)
        font = cv2.FONT_HERSHEY_SIMPLEX
        org = (50, 50)
        fontScale = 1
        color = (0,0,255)
        thickness = 2
        cv2.putText(TUMOR_IMAGE, 'Tumor  Exist', org, font,
                    fontScale, color, thickness, cv2.LINE_AA)
        cv2.imwrite(("Detection_Images/" + Image),TUMOR_IMAGE)
        f,updated = Tumor_Detection(Tumor_Image)
        cv2.imwrite(("New_Images/" + Image), updated)
    ############################################################################################