import { useState } from 'react';
import { Upload, Card, Alert, Progress, Table } from 'antd';
import { InboxOutlined, DeleteOutlined, CheckCircleOutlined } from '@ant-design/icons';
import { useDispatch, useSelector } from 'react-redux';
import type { AppDispatch, RootState } from '../store';
import { uploadFile, setLoading, setError, setSourceData } from '../store/slices/enrollmentSlice';
import { uploadAPI } from '../services/api';
import type { UploadFile, UploadProps } from 'antd/es/upload/interface';

const { Dragger } = Upload;

export default function FileUpload() {
  const dispatch = useDispatch<AppDispatch>();
  const { uploadedFile, loading, error } = useSelector((state: RootState) => state.enrollment);
  const [preview, setPreview] = useState<any[]>([]);
  const [fileList, setFileList] = useState<UploadFile[]>([]);

  const handleUpload = async (file: File) => {
    dispatch(uploadFile(file));
    
    try {
      dispatch(setLoading(true));
      const response = await uploadAPI.parseFile(file);
      const { data, preview: previewData } = response.data;
      
      setPreview(previewData || data.slice(0, 5)); // Show first 5 rows as preview
      dispatch(setSourceData(data));
      dispatch(setLoading(false));
    } catch (err: any) {
      dispatch(setError(err.response?.data?.error || err.message || 'Failed to parse file'));
      setFileList([]);
    }
  };

  const uploadProps: UploadProps = {
    name: 'file',
    multiple: false,
    accept: '.xlsx,.xls,.csv',
    fileList,
    beforeUpload: (file) => {
      handleUpload(file);
      setFileList([{
        uid: file.name,
        name: file.name,
        status: 'uploading',
        originFileObj: file,
      }]);
      return false; // Prevent default upload
    },
    onRemove: () => {
      dispatch(uploadFile(null as any));
      setPreview([]);
      setFileList([]);
    },
    showUploadList: {
      showRemoveIcon: true,
      removeIcon: <DeleteOutlined />,
    },
  };

  const clearFile = () => {
    dispatch(uploadFile(null as any));
    setPreview([]);
    setFileList([]);
  };

  // Create columns for preview table
  const previewColumns = preview.length > 0 
    ? Object.keys(preview[0]).map(key => ({
        title: key,
        dataIndex: key,
        key,
        ellipsis: true,
      }))
    : [];

  const previewData = preview.map((row, index) => ({
    ...row,
    key: index,
  }));

  return (
    <Card title="Upload Source Data" className="mb-6">
      {error && (
        <Alert
          message="Upload Error"
          description={error}
          type="error"
          showIcon
          closable
          className="mb-4"
          onClose={() => dispatch(setError(''))}
        />
      )}

      <Dragger {...uploadProps} style={{ marginBottom: preview.length > 0 ? 24 : 0 }}>
        <p className="ant-upload-drag-icon">
          <InboxOutlined />
        </p>
        <p className="ant-upload-text">Click or drag file to this area to upload</p>
        <p className="ant-upload-hint">
          Supports Excel (.xlsx, .xls) and CSV files. Single file upload only.
        </p>
      </Dragger>

      {loading && (
        <div className="mb-4">
          <Progress percent={undefined} status="active" />
          <p className="text-sm text-gray-500 mt-2">Processing file...</p>
        </div>
      )}

      {uploadedFile && !loading && (
        <Alert
          message="File processed successfully"
          type="success"
          showIcon
          icon={<CheckCircleOutlined />}
          className="mb-4"
        />
      )}

      {preview.length > 0 && (
        <div>
          <h3 className="text-base font-medium mb-3">Preview (First 5 rows)</h3>
          <Table
            columns={previewColumns}
            dataSource={previewData}
            pagination={false}
            scroll={{ x: true }}
            size="small"
            bordered
          />
        </div>
      )}
    </Card>
  );
}
