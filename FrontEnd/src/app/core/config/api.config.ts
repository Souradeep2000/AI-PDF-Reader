import { environment } from '../../../environments/environment';
import { provideHttpClient } from '@angular/common/http';

export const API_CONFIG = {
  BASE_URL: environment.apiBaseUrl,

  ENDPOINTS: {
    ASK: '/ask',
    ASK_STREAM: '/ask-stream',
    UPLOAD: '/upload',
    SEARCH: '/search',
  },

  providers: [provideHttpClient()],
};
