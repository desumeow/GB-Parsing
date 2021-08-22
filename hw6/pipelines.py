import scrapy
from scrapy.pipelines.files import FilesPipeline
from scrapy.pipelines.images import ImagesPipeline
from os.path import splitext
from scrapy import Request

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

class LmImagesPipeLine(FilesPipeline):

    def get_media_requests(self, item, info):
        return [Request(x, meta={'file_name': item.get('file_name')}) for x in item.get(self.files_urls_field, [])]

    def file_path(self, request, response=None, info=None):
        url = request.url
        media_ext = splitext(url)[1]
        return f'full\\{request.meta["filename"]}{media_ext}'

# class AvitoAutoImagePipeline(ImagesPipeline):
#     def get_media_requests(self, item, info):
#         if item['files']:
#             for img in item['files']:
#                 try:
#                     yield scrapy.Request(img)
#                 except TypeError as e:
#                     print(e)
#         return item