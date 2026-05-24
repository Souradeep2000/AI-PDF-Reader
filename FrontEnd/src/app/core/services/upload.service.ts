import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpEventType, HttpEvent } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { API_CONFIG } from '../config/api.config';

@Injectable({
  providedIn: 'root',
})
export class UploadService {
  private http = inject(HttpClient);
  private baseUrl = `${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.UPLOAD}`;

  // Change parameter to take a single File item
  uploadSingleFile(
    file: File,
  ): Observable<{ type: 'progress' | 'done'; value: number | any }> {
    const formData = new FormData();

    // CRITICAL: Name must be 'file' to match FastAPI's parameter name!
    formData.append('file', file);

    return this.http
      .post(this.baseUrl, formData, {
        reportProgress: true,
        observe: 'events',
      })
      .pipe(
        map((event: HttpEvent<any>) => {
          switch (event.type) {
            case HttpEventType.UploadProgress:
              const progress = event.total
                ? Math.round((100 * event.loaded) / event.total)
                : 0;
              return { type: 'progress', value: progress };
            case HttpEventType.Response:
              return { type: 'done', value: event.body };
            default:
              return { type: 'progress', value: 0 };
          }
        }),
      );
  }
}
