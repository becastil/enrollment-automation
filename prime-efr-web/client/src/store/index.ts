import { configureStore } from '@reduxjs/toolkit';
import enrollmentReducer from './slices/enrollmentSlice';
import validationReducer from './slices/validationSlice';
import configReducer from './slices/configSlice';

export const store = configureStore({
  reducer: {
    enrollment: enrollmentReducer,
    validation: validationReducer,
    config: configReducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: {
        // Ignore these action types for File objects
        ignoredActions: ['enrollment/uploadFile'],
        ignoredActionPaths: ['payload.file'],
        ignoredPaths: ['enrollment.uploadedFile'],
      },
    }),
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;