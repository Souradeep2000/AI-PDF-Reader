export interface SSEEvent {
  event: string;
  data: string;
}

export class SSEParser {
  private buffer = '';
  private currentEvent = 'message'; // Default fallback event name

  parse(chunk: string): SSEEvent[] {
    this.buffer += chunk;
    const events: SSEEvent[] = [];

    // Split by single newlines to process line-by-line immediately
    const lines = this.buffer.split('\n');

    // Keep the last incomplete line in the buffer
    this.buffer = lines.pop() ?? '';

    for (const line of lines) {
      const cleanLine = line.trim();

      // If we encounter an empty line, it signals an SSE boundary, but we can also emit on data receipt
      if (!cleanLine) continue;

      if (cleanLine.startsWith('event:')) {
        this.currentEvent = cleanLine.replace('event:', '').trim();
      } else if (cleanLine.startsWith('data:')) {
        // Use substring to safely extract all text after "data:"
        // Slice off "data:" and drop only leading spaces up to the first actual character
        const dataValue = line.substring(5).replace(/^\s/, '');

        events.push({
          event: this.currentEvent,
          data: dataValue,
        });

        // Reset tracking back to default for the next event block
        this.currentEvent = 'message';
      }
    }

    return events;
  }
}
