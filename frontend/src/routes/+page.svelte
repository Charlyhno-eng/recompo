<script lang="ts">
    import Navbar from "$lib/components/layout/Navbar.svelte";
    import UploadForm from "$lib/components/ui/UploadForm.svelte";

    let audioFile: File | null = null;
    let videoFile: File | null = null;
    const minParts = 1;
    const maxParts = 30;

    let parts: number = minParts;
    let isLoading = false;
    let currentSegment = 0;

    let progressInterval: number | null = null;

    function startProgressPolling() {
        stopProgressPolling();
        progressInterval = window.setInterval(async () => {
            const res = await fetch("http://localhost:8000/progress");
            if (!res.ok) return;
            const data = await res.json();
            currentSegment = data.current ?? 0;
        }, 800);
    }

    function stopProgressPolling() {
        if (progressInterval !== null) {
            clearInterval(progressInterval);
            progressInterval = null;
        }
    }

    function onAudioChange(e: Event) {
        const target = e.currentTarget as HTMLInputElement;
        audioFile = target.files?.[0] ?? null;
    }

    function onVideoChange(e: Event) {
        const target = e.currentTarget as HTMLInputElement;
        videoFile = target.files?.[0] ?? null;
    }

    async function handleSubmit(event: SubmitEvent) {
        event.preventDefault();
        if (!audioFile || !videoFile || isLoading) return;

        isLoading = true;
        currentSegment = 0;
        startProgressPolling();

        const formData = new FormData();
        formData.append("audio", audioFile);
        formData.append("video", videoFile);
        formData.append("parts", String(parts));

        try {
            const res = await fetch("http://localhost:8000/generate", {
                method: "POST",
                body: formData,
            });

            if (!res.ok) {
                console.error("Backend error", await res.text());
                return;
            }

            const blob = await res.blob();
            const url = URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.href = url;
            a.download = "videos.zip";
            document.body.appendChild(a);
            a.click();
            a.remove();
            URL.revokeObjectURL(url);
        } finally {
            stopProgressPolling();
            isLoading = false;
            currentSegment = parts;
        }
    }
</script>

<main class="min-h-screen flex flex-col">
    <Navbar />

    <UploadForm
        bind:parts
        {audioFile}
        {videoFile}
        {minParts}
        {maxParts}
        {isLoading}
        {currentSegment}
        {onAudioChange}
        {onVideoChange}
        onSubmit={handleSubmit}
    />
</main>
