import { ytDownload } from 'https://deno.land/x/yt_download/mod.ts';

const port = 8080;
const hostname = '0.0.0.0';

const downloadVideo = async (url: string, dir: string, filename: string, format: string): Promise<void> => {
    url = url.replace('https://www.youtube.com/watch?v=', '');

    try {
        await Deno.mkdir(dir, { recursive: true });

        let stream;
        if (format === 'MP3') {
            stream = await ytDownload(url, {
                hasVideo: false,
                hasAudio: true,
            });
        } else {
            stream = await ytDownload(url);
        }

        const filePath = (format === 'MP3') ? `${dir}/${filename}.mp3` : `${dir}/${filename}.mp4`;

        const file = await Deno.open(filePath, {
            create: true,
            write: true,
            truncate: true,
        });

        try {
            const reader = stream.getReader();
            const writer = file.write.bind(file);
            let result = await reader.read();
            while (!result.done) {
                const chunk = result.value;
                await writer(chunk);
                result = await reader.read();
            }
        } finally {
            file.close();
        }
    } catch (error) {
        console.error(`Error downloading video from ${url}:`, error);
        throw error;
    }
};

const handler = async (req: Request): Promise<Response> => {
    const url = new URL(req.url);

    if (req.method === 'OPTIONS') {
        return new Response(null, {
            headers: {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type',
            },
        });
    }

    if (req.method === 'GET' && url.pathname === '/') {
        try {
            const filePath = './index.html';
            const file = await Deno.open(filePath);
            const content = await Deno.readAll(file);
            file.close();

            return new Response(content, {
                headers: {
                    'Content-Type': 'text/html',
                    'Access-Control-Allow-Origin': '*',
                },
            });
        } catch (error) {
            console.error(`Error serving index.html:`, error);
            return new Response('Internal Server Error', { status: 500, headers: { 'Access-Control-Allow-Origin': '*' } });
        }
    }

    if (req.method === 'GET' && url.pathname.startsWith('/img/')) {
        try {
            const filePath = `.${url.pathname}`;
            const file = await Deno.open(filePath);
            const content = await Deno.readAll(file);
            file.close();

            const contentType = url.pathname.endsWith('.svg') ? 'image/svg+xml' : 'application/octet-stream';

            return new Response(content, {
                headers: {
                    'Content-Type': contentType,
                    'Access-Control-Allow-Origin': '*',
                },
            });
        } catch (error) {
            console.error(`Error serving image ${url.pathname}:`, error);
            return new Response('Not Found', { status: 404, headers: { 'Access-Control-Allow-Origin': '*' } });
        }
    }

    if (req.method === 'POST' && url.pathname === '/download') {
        try {
            const { urls, format, directory } = await req.json();
            
            if (urls && Array.isArray(urls) && urls.length > 0 && directory) {
                await Promise.all(urls.map((url, index) => downloadVideo(url, directory, `downloaded_video_${index + 1}`, format)));

                return new Response('Download started', {
                    status: 200,
                    headers: {
                        'Content-Type': 'text/plain',
                        'Access-Control-Allow-Origin': '*', 
                    },
                });
            } else {
                console.error('Invalid request data:', { urls, format, directory });
                return new Response('Invalid request data', { status: 400, headers: { 'Access-Control-Allow-Origin': '*' } });
            }
        } catch (error) {
            console.error('Error processing download request:', error);
            return new Response('Error processing request', { status: 500, headers: { 'Access-Control-Allow-Origin': '*' } });
        }
    }

    return new Response('Method not allowed', { status: 405, headers: { 'Access-Control-Allow-Origin': '*' } });
};

console.log(`Server running on http://${hostname}:${port}/`);
Deno.serve({ hostname, port }, handler);