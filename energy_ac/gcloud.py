from google.cloud import vision

def detect_text(image):
    client = vision.ImageAnnotatorClient()

    path = '/home/josbal69/code/Josbal69/energyac/foto1martin.jpeg'

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations
    print('texts:')
    words_dict={}
    words_list=[]

    for text in texts:
        print('\n"{}"'.format(text.description))

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in text.bounding_poly.vertices])

        print('bounds: {}'.format(','.join(vertices)))

        words_dict[text.description]=list(vertices)
        words_list.append(text.description)

    data_photo = []
    for word in words_list:
        if ((len(word)>2 & len(word)< 5) & (word[0]>"1") & ( word[0]< "8")):
            if word[1] == ",":
                data_photo.append(word)
    photo_dic = {}
    photo_dic['Cap_Refrig'] = data_photo[0]
    photo_dic['ERR'] = data_photo[1]

    return photo_dic
