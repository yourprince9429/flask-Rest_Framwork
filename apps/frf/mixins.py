from .response_code import RET
from flask import jsonify
from sqlalchemy.exc import SQLAlchemyError
from .framework import APIView


class ListAPIView(object):
    def add_data_list(self, data_dict):

        return data_dict

    def get(self):
        request_data = self.get_request_data()
        serializer = self.get_serializer_class()
        request_data = serializer.validate(data=request_data)

        page_num = None
        size = None
        error = False
        if request_data is not None:
            page_num = request_data.pop(self.paginate_field[0], None)
            size = request_data.pop(self.paginate_field[1], None)
            error = request_data.pop(self.paginate_field[2], False)

        # self.look_up = request_data
        filter_queryset = self.filter_queryset()
        if page_num and size:
            page_data = self.list_paginate(filter_queryset, page_num, size, error)
            all_data = page_data.items
            total = page_data.total
        else:
            all_data = filter_queryset.all()

        if not all_data:
            return jsonify(code=RET.NODATA, msg='没有数据', data="")

        data_list = []
        serializer = self.get_serializer_class()
        for instance in all_data:
            instance_dict = {field: getattr(instance, field, None) for field in serializer.all_fields}
            data_dict = serializer.serialize_return_data(instance_dict)
            self.add_data_list(data_dict)
            data_list.append(data_dict)

        try:
            total
        except:
            return jsonify(code=RET.OK, msg="ok", data=data_list)
        else:
            return jsonify(code=RET.OK, msg="ok", data=data_list, total=total)


class RetrieveAPIView(object):
    def add_data_instance(self, data_dict):
        return data_dict

    def retrieve(self):
        request_data = self.request_data
        pk = request_data.get(self.pk_field)
        if not pk:
            return jsonify(code=RET.PARAMERR, msg="参数错误", data="")
        pk_field_dict = {self.pk_field: pk}
        instance = self.filter_queryset().filter_by(**pk_field_dict).first()
        if not instance:
            return jsonify(code=RET.NODATA, msg='没有数据', data="")
        serializer = self.get_serializer_class()
        instance_dict = {field: getattr(instance, field, None) for field in serializer.all_fields}
        data = serializer.serialize_return_data(instance_dict)
        data = self.add_data_instance(data)
        return jsonify(code=RET.OK, msg='ok', data=data)


class CreateAPIView(object):
    def post(self):
        # 获取参数
        request_data = self.request_data
        if isinstance(request_data, list):
            if self.bulk_save(request_data):
                return jsonify(code=RET.OK, msg='ok', data="")
            else:
                return jsonify(code=RET.DBERR, msg='dberror', data="")
        try:
            serializer, instance = self.perform_save(request_data)
        except SQLAlchemyError:
            return jsonify(code=RET.DBERR, msg='数据库错误', data="")
        except TypeError:
            return jsonify(code=RET.PARAMERR, msg='参数错误', data="")
        except AttributeError:
            return jsonify(code=RET.PARAMERR, msg='参数不齐', data="")
        except Exception as e:
            return jsonify(code=RET.UNKOWNERR, msg='未知错误', data=e.__str__())
        # 返回保存的这条数据的信息
        instance_dict = {field: getattr(instance, field, None) for field in serializer.all_fields}
        data = serializer.serialize_return_data(instance_dict)
        data = self.add_data_post(data)
        return jsonify(code=RET.OK, msg='ok', data=data)

    def add_data_post(self, data_dict):
        return data_dict


class UpdateAPIView(object):
    def put(self):
        request_data = self.get_request_data()

        filter_data = request_data.get(self.pk_field)
        print(filter_data)
        try:
            instance = self.get_instance(filter_data={self.pk_field: filter_data})
        except SQLAlchemyError:
            return jsonify(code=RET.DBERR, msg='查询数据异常', data="")
        if not instance:
            return jsonify("未查找到数据")
        try:
            serializer, instance = self.perform_save(request_data, instance)
        except SQLAlchemyError:
            return jsonify(code=RET.DBERR, msg='数据库错误', data="")
        except TypeError:
            return jsonify(code=RET.PARAMERR, msg='参数错误', data="")
        except AttributeError:
            return jsonify(code=RET.PARAMERR, msg='参数不齐', data="")
        except Exception as e:
            return jsonify(code=RET.UNKOWNERR, msg='未知错误', data=e.__str__())
        try:
            instance_dict = {field: getattr(instance, field, None) for field in serializer.all_fields}
        except SQLAlchemyError:
            return jsonify(code=RET.DBERR, msg='数据库错误', data="")

        data = serializer.serialize_return_data(instance_dict)
        if not data:
            return jsonify(code=RET.NODATA, msg="没有数据", data="")
        data = self.add_data_put(data)
        return jsonify(code=RET.OK, msg='ok', data=data)

    def patch(self):
        request_data = self.get_request_data()

        filter_data = request_data.get(self.pk_field)
        try:
            instance = self.get_instance(filter_data={self.pk_field: filter_data})
        except SQLAlchemyError:
            return jsonify(code=RET.DBERR, msg='数据库查询错误', data="")
        if not instance:
            return jsonify("未查找到数据")
        try:
            serializer, instance = self.perform_save(request_data, instance)
        except SQLAlchemyError:
            return jsonify(code=RET.DBERR, msg='数据库错误', data="")
        except TypeError:
            return jsonify(code=RET.PARAMERR, msg='参数错误', data="")
        except AttributeError:
            return jsonify(code=RET.PARAMERR, msg='参数不齐', data="")
        except Exception as e:
            return jsonify(code=RET.UNKOWNERR, msg='未知错误', data=e.__str__())

        instance_dict = {field: getattr(instance, field, None) for field in serializer.all_fields}
        data = serializer.serialize_return_data(instance_dict)
        if not data:
            return jsonify(code=RET.NODATA, msg="没有数据", data="")
        data = self.add_data_put(data)
        return jsonify(code=RET.OK, msg='ok', data=data)

    def add_data_put(self, data_dict):
        return data_dict


class DeleteAPIView(object):
    def delete(self):
        request_data = self.request_data
        if isinstance(request_data, list):
            if self.bulk_delete(request_data):
                return jsonify(code=RET.OK, msg='ok', data="")
            else:
                return jsonify(code=RET.DBERR, msg='数据库错误', data="")

        filter_data = request_data.get(self.pk_field)
        try:
            instance = self.get_instance(filter_data={self.pk_field: filter_data})
        except SQLAlchemyError:
            return jsonify(code=RET.DBERR, msg='数据查询错误', data="")
        if not instance:
            return None
        self.perform_delete(instance)
        return jsonify(code=RET.OK, msg='ok', data="")


class ReadOnlyMixin(RetrieveAPIView, ListAPIView, APIView):
    """
    只读方法
    """
    pass


class AllMethodMixin(ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DeleteAPIView, APIView):
    """
    所有方法
    """
    pass
