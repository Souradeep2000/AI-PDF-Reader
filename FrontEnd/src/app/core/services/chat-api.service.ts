import { Injectable } from '@angular/core';
import { API_CONFIG } from '../config/api.config';
import { SSEParser } from '../utils/sse-parser';

@Injectable({
  providedIn: 'root',
})
export class ChatApiService {
  async streamAsk(
    query: string,
    topK: number = 5,
    onToken: (token: string) => void,
  ): Promise<any> {
    const url = `${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.ASK_STREAM}`;

    console.log('--- [STEP 1: NETWORK TRIGGER] Sending request to:', url);

    const response = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query, top_k: topK }),
    });

    if (!response.body) {
      console.error('--- [ERROR] Response body is empty/null.');
      throw new Error('No response body');
    }

    console.log('--- [STEP 2: HTTP CONNECTED] Status:', response.status);

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    const parser = new SSEParser();
    let finalResponse = null;
    let chunkCount = 0;

    while (true) {
      const { done, value } = await reader.read();
      if (done) {
        console.log('--- [STEP 5: STREAM FINISHED] Reader loop closed.');
        break;
      }

      chunkCount++;
      const chunk = decoder.decode(value, { stream: true });
      console.log(
        `--- [STEP 3: RAW CHUNK #${chunkCount}] Length:`,
        chunk.length,
        '\nRaw String:',
        chunk,
      );

      const events = parser.parse(chunk);
      console.log(
        `--- [STEP 4: PARSER OUTPUT for Chunk #${chunkCount}] Events found:`,
        events.length,
        events,
      );

      for (const event of events) {
        if (event.event === 'token') {
          console.log(
            `🚀 Triggering onToken() callback with value: "${event.data}"`,
          );
          onToken(event.data);
        }
        if (event.event === 'done') {
          console.log(
            '🏁 Stream structural end payload found ("done"):',
            event.data,
          );
          finalResponse = JSON.parse(event.data);
        }
      }
    }

    return finalResponse;
  }
}
