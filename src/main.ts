// deno-lint-ignore-file
import { ytDownload, getVideoInfo } from "https://deno.land/x/yt_download@1.10/mod.ts";
import { readAll } from "https://deno.land/std@0.224.0/io/read_all.ts";

const port = 8080;
const hostname = '0.0.0.0';

const convertMp4ToMp3 = async (inputFile: string, outputFile: string) => {
    const ffmpegCommand = [
        "ffmpeg",
        "-i", inputFile,
        "-q:a", "0",
        "-map", "a",
        outputFile
    ];

    const process = Deno.run({
        cmd: ffmpegCommand,
        stderr: "piped",
        stdout: "piped"
    });

    const { code } = await process.status();
    if (code !== 0) {
        const error = new TextDecoder().decode(await process.stderrOutput());
        throw new Error(`ffmpeg error: ${error}`);
    }

    process.close();
};

const downloadVideo = async (url: string, dir: string, format: string): Promise<void> => {
    url = url.replace('https://www.youtube.com/watch?v=', '');
    let filename = url;

    try {
        await Deno.mkdir(dir, { recursive: true });

        const metadata: any = await getVideoInfo(url);
        const title = metadata.microformat.playerMicroformatRenderer.title.simpleText.replace(/[<>:"\/\\|?*\x00-\x1F]/g, '');
        filename = title;

        let stream;
        if (format === 'MP3') {
            const mp4FilePath = `${dir}/${filename}.mp4`;
            const mp3FilePath = `${dir}/${filename}.mp3`;

            stream = await ytDownload(url);
            const file = await Deno.open(mp4FilePath, {
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

            await convertMp4ToMp3(mp4FilePath, mp3FilePath);
            await Deno.remove(mp4FilePath); 

        } else {
            stream = await ytDownload(url);
            const filePath = `${dir}/${filename}.mp4`;

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
            const content = await readAll(file);
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

    if (req.method === 'GET' && url.pathname.startsWith('/assets/')) {
        try {
            const filePath = `/app${url.pathname}`;
            const file = await Deno.open(filePath);
            const content = await readAll(file);
            file.close();

            const contentType = url.pathname.endsWith('.svg') ? 'image/svg+xml' : 
                                url.pathname.endsWith('.png') ? 'image/png' : 
                                'application/octet-stream';

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
            const containerDir = '/app/downloads'; 
            
            if (urls && Array.isArray(urls) && urls.length > 0 && directory) {
                await Deno.mkdir(directory, { recursive: true });

                await Promise.all(urls.map((url) => downloadVideo(url, containerDir, format)));
                
                return new Response('Download completed and files moved', {
                    status: 200,
                    headers: {
                        'Content-Type': 'text/plain',
                        'Access-Control-Allow-Origin': '*', 
                    },
                });
            } else {
                return new Response('Invalid request', {
                    status: 400,
                    headers: {
                        'Content-Type': 'text/plain',
                        'Access-Control-Allow-Origin': '*', 
                    },
                });
            }
        } catch (error) {
            console.error(`Error processing download:`, error);
            return new Response('Error processing request', {
                status: 500,
                headers: {
                    'Content-Type': 'text/plain',
                    'Access-Control-Allow-Origin': '*', 
                },
            });
        }
    }

    return new Response('Method not allowed', { status: 405, headers: { 'Access-Control-Allow-Origin': '*' } });
};

console.log(`Server running on http://${hostname}:${port}/`);
Deno.serve({ hostname, port }, handler);