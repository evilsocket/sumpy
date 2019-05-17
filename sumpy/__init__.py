import os
import sys

sys.path.insert(0, os.path.dirname(__file__) + '/proto')

import zlib
import grpc
import json

import sumpy.proto.sum_pb2 as protocol
import sumpy.proto.sum_pb2_grpc as proto_svc

__author__    = 'Simone Margaritelli'
__email__     = 'evilsocket@gmail.com'
__copyright__ = 'Copyright 2019, Simone Margaritelli'
__license__   = 'GPL3'
__version__   = '1.3.3'
__status__    = 'Production'

MAX_MESSAGE_SIZE = 10 * 1024 * 1024
DEFAULT_OPTIONS  = [('grpc.max_send_message_length', MAX_MESSAGE_SIZE), 
                    ('grpc.max_receive_message_length', MAX_MESSAGE_SIZE)]

class Client:
    def __init__(self, connection, certificate, opts = DEFAULT_OPTIONS):
        self._conn_str = connection
        self._opts = opts

        with open(certificate, 'rb') as fp:
            cert = fp.read()

        self._creds = grpc.ssl_channel_credentials(root_certificates=cert)
        self._channel = grpc.secure_channel(self._conn_str, self._creds, options=self._opts)
        self._rpc = proto_svc.SumServiceStub(self._channel)
    
    def _check_resp(self, r):
        if r.success == False:
            raise Exception(r.msg)

    def _get_oracle_payload(self, data):
        raw = data.payload
        if data.compressed:
            raw = zlib.decompress(raw, 16+zlib.MAX_WBITS)
        return json.loads(raw)

    def create_record(self, meta, data):
        record = protocol.Record(data=data, meta=meta)
        resp = self._rpc.CreateRecord(record)
        self._check_resp(resp)
        record.id = int(resp.msg)
        return record 

    def update_record(self, id, meta, data):
        record = protocol.Record(id=id, data=data, meta=meta)
        resp = self._rpc.UpdateRecord(record)
        self._check_resp(resp)
        return resp.success 
    
    def read_record(self, identifier):
        resp = self._rpc.ReadRecord(protocol.ById(id=int(identifier)))
        self._check_resp(resp)
        return resp.record

    def list_records(self, page, per_page):
        return self._rpc.ListRecords(protocol.ListRequest( \
            page=page,
            per_page=per_page))

    def delete_record(self, identifier):
        resp = self._rpc.DeleteRecord(protocol.ById(id=identifier))
        self._check_resp(resp)

    def find_records(self, meta, value):
        resp = self._rpc.FindRecords(protocol.ByMeta(meta=meta, value=value))
        self._check_resp(resp)
        return resp.records

    def define_oracle_code(self, name, code):
        oracle = protocol.Oracle(name=name, code=code)
        resp = self._rpc.CreateOracle(oracle)
        self._check_resp(resp)
        return int(resp.msg)

    def define_oracle(self, name, filename):
        with open( filename, 'r') as fp:
            return self.define_oracle_code(name, fp.read())

    def read_oracle(self, identifier):
        resp = self._rpc.ReadOracle(protocol.ById(id=int(identifier)))
        self._check_resp(resp)
        return resp.oracle

    def find_oracle(self, name):
        resp = self._rpc.FindOracle(protocol.ByName(name=name))
        self._check_resp(resp)
        return resp.oracle

    def list_oracles(self, page, per_page):
        return self._rpc.ListOracles(protocol.ListRequest( \
            page=page,
            per_page=per_page))

    def delete_oracle(self, identifier):
        resp = self._rpc.DeleteOracle(protocol.ById(id=identifier))
        self._check_resp(resp)

    def invoke_oracle(self, oracle_id, args):
        resp = self._rpc.Run(protocol.Call(oracle_id=oracle_id, args=map(json.dumps, args)))
        self._check_resp(resp)
        return self._get_oracle_payload(resp.data)


