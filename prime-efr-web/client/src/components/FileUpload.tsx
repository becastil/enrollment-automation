import { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, FileSpreadsheet, X, CheckCircle } from 'lucide-react';
import { useDispatch, useSelector } from 'react-redux';
import type { AppDispatch, RootState } from '../store';
import { uploadFile, setLoading, setError, setSourceData } from '../store/slices/enrollmentSlice';
import { uploadAPI } from '../services/api';

export default function FileUpload() {
  const dispatch = useDispatch<AppDispatch>();
  const { uploadedFile, loading, error } = useSelector((state: RootState) => state.enrollment);
  const [preview, setPreview] = useState<any[]>([]);

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    if (acceptedFiles.length === 0) return;
    
    const file = acceptedFiles[0];
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
    }
  }, [dispatch]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/vnd.ms-excel': ['.xls'],
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx'],
      'text/csv': ['.csv'],
    },
    maxFiles: 1,
  });

  const clearFile = () => {
    dispatch(uploadFile(null as any));
    setPreview([]);
  };

  return (
    <div className="card">
      <h2 className="text-xl font-semibold mb-md">Upload Source Data</h2>
      
      {!uploadedFile ? (
        <div
          {...getRootProps()}
          className={`border-2 border-dashed rounded-lg p-xl text-center cursor-pointer transition-colors ${
            isDragActive
              ? 'border-primary bg-primary-soft'
              : 'border-border hover:border-border-strong hover:bg-surface-subtle'
          }`}
        >
          <input {...getInputProps()} />
          <Upload className="mx-auto h-12 w-12 text-text-muted mb-md" />
          <p className="text-text-muted mb-xs">
            {isDragActive
              ? 'Drop the file here...'
              : 'Drag and drop your Excel file here, or click to browse'}
          </p>
          <p className="text-sm text-text-muted">
            Supports .xlsx, .xls, and .csv files
          </p>
        </div>
      ) : (
        <div className="space-y-md">
          <div className="flex items-center justify-between p-md bg-surface-subtle rounded-lg">
            <div className="flex items-center">
              <FileSpreadsheet className="h-8 w-8 text-primary mr-sm" />
              <div>
                <p className="font-medium text-text">{uploadedFile.name}</p>
                <p className="text-sm text-text-muted">
                  {(uploadedFile.size / 1024).toFixed(2)} KB
                </p>
              </div>
            </div>
            <button
              onClick={clearFile}
              className="p-xs hover:bg-surface rounded-lg transition-colors"
            >
              <X className="h-5 w-5 text-text-muted" />
            </button>
          </div>
          
          {loading && (
            <div className="text-center py-md">
              <div className="inline-flex items-center">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
                <span className="ml-sm text-text-muted">Processing file...</span>
              </div>
            </div>
          )}
          
          {error && (
            <div className="alert-error">
              <p className="font-medium">Error processing file</p>
              <p className="text-sm mt-xs">{error}</p>
            </div>
          )}
          
          {preview.length > 0 && !loading && !error && (
            <div>
              <div className="flex items-center mb-xs">
                <CheckCircle className="h-5 w-5 text-success mr-xs" />
                <p className="font-medium text-text">File parsed successfully</p>
              </div>
              <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-border">
                  <thead className="bg-surface-subtle">
                    <tr>
                      {Object.keys(preview[0] || {}).map((key) => (
                        <th
                          key={key}
                          className="px-sm py-xs text-left text-xs font-medium text-text-muted uppercase"
                        >
                          {key}
                        </th>
                      ))}
                    </tr>
                  </thead>
                  <tbody className="bg-surface divide-y divide-border">
                    {preview.map((row, idx) => (
                      <tr key={idx}>
                        {Object.values(row).map((val: any, i) => (
                          <td key={i} className="px-sm py-xs text-sm text-text">
                            {val}
                          </td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
              <p className="text-sm text-text-muted mt-sm">
                Showing first 5 rows of {preview.length} total
              </p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
