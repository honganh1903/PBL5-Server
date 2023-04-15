from flask import Blueprint, request, jsonify, send_file
from firebase_admin import storage, db
from datetime import datetime, timedelta


imageAPI = Blueprint('imageAPI', __name__)


@imageAPI.route('/', methods=['POST'])
# def upload_image():
#     image = request.files['image']
#     image_data = image.read()
#     image_name = "Fire_Detection/" + image.filename
#     image_content_type = image.content_type
#
#     bucket = storage.bucket()
#     blob = bucket.blob(image_name)
#     blob.upload_from_string(image_data, content_type=image_content_type)
#     url = blob.generate_signed_url(
#         version='v4',
#         expiration=datetime.timedelta(minutes=15),
#         method='GET'
#     )
#
#
#     # Trả về link của ảnh
#     return jsonify({'url': url})
def upload_image_and_create_item():
    # Lấy file ảnh từ form data
    image = request.files['image']
    image_data = image.read()
    image_name = "Fire_Detection/" + image.filename
    image_content_type = image.content_type

    # Tải ảnh lên Firebase Storage
    bucket = storage.bucket()
    blob = bucket.blob(image_name)
    blob.upload_from_string(image_data, content_type=image_content_type)
    url = blob.generate_signed_url(
        version='v4',
        expiration=timedelta(minutes=15),
        method='GET'
    )

    # Lấy dữ liệu từ form data và thêm thuộc tính 'date' vào
    item = {}
    item['date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    item['imageUrl'] = url
    item['status'] = True

    # Tải dữ liệu lên Firebase Realtime Database
    ref = db.reference('user')
    new_item_ref = ref.push()
    new_item_ref.set(item)

    return jsonify({'message': 'Created successfully', 'item_id': new_item_ref.key}), 201

@imageAPI.route('/<image_name>', methods=['GET'])
def get_image(image_name):
    bucket = storage.bucket()
    blob = bucket.blob('Fire_Detection/' + image_name)
    if not blob.exists():
        return jsonify({'error': 'Image does not exist'})
    url = blob.generate_signed_url(
        version='v4',
        expiration=datetime.timedelta(minutes=15),
        method='GET'
    )
    return jsonify({'url': url})