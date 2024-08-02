import { ytDownload } from 'https://deno.land/x/yt_download/mod.ts';

const port = 8080;

const downloadVideo = async (url: string, dir: string, filename: string): Promise<void> => {
    url = url.replace('https://www.youtube.com/watch?v=', '');

    await Deno.mkdir(dir, { recursive: true });

    const filePath = `${dir}/${filename}.mp4`;
    const stream = await ytDownload(url);
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
};

const handler = async (req: Request): Promise<Response> => {
    const url = new URL(req.url);

    if (req.method === 'OPTIONS') {
        return new Response(null, {
            headers: {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type',
            },
        });
    }

    if (req.method === 'POST') {
        try {
            const { urls, directory } = await req.json();
            if (urls && Array.isArray(urls) && urls.length > 0 && directory) {
                await Promise.all(urls.map((url, index) => downloadVideo(url, directory, `downloaded_video_${index + 1}`)));
                return new Response('Download started', {
                    status: 200,
                    headers: {
                        'Content-Type': 'text/plain',
                        'Access-Control-Allow-Origin': '*', 
                    },
                });
            } else {
                return new Response('Invalid request data', { status: 400, headers: { 'Access-Control-Allow-Origin': '*' } });
            }
        } catch (error) {
            return new Response('Error processing request', { status: 500, headers: { 'Access-Control-Allow-Origin': '*' } });
        }
    }

    return new Response('Method not allowed', { status: 405, headers: { 'Access-Control-Allow-Origin': '*' } });
};

Deno.serve({ port }, handler);