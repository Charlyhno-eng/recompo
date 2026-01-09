<script lang="ts">
    let audioFile: File | null = null;
    let videoFile: File | null = null;
    let parts = 10;
    let isLoading = false;

    const minParts = 2;
    const maxParts = 30;

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
                console.error("Erreur backend", await res.text());
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
            isLoading = false;
        }
    }
</script>

<main class="min-h-screen flex items-center justify-center px-4">
    <section
        class="card w-full max-w-xl preset-filled-surface-900-950/80 border border-primary-500/40 shadow-xl rounded-2xl p-6 sm:p-8 space-y-6 backdrop-blur"
    >
        <header class="space-y-2 text-center">
            <h1 class="text-2xl sm:text-3xl font-semibold text-surface-900">
                Génération de vidéos sous-titrées
            </h1>
            <p class="text-sm text-surface-500">
                Ajoute ton audio, ton GIF ou MP4, choisis le nombre de vidéos,
                et on s’occupe du reste.
            </p>
        </header>

        <form class="space-y-5" on:submit|preventDefault={handleSubmit}>
            <div class="space-y-2 text-left">
                <label
                    for="audio"
                    class="block text-sm font-medium text-surface-700"
                >
                    Fichier audio (MP3)
                </label>
                <input
                    id="audio"
                    type="file"
                    accept="audio/mpeg,audio/mp3"
                    class="input w-full preset-outline-surface-50-900"
                    on:change={onAudioChange}
                    required
                    disabled={isLoading}
                />
                {#if audioFile}
                    <p class="text-xs text-surface-500">
                        Sélectionné : {audioFile.name}
                    </p>
                {/if}
            </div>

            <div class="space-y-2 text-left">
                <label
                    for="video"
                    class="block text-sm font-medium text-surface-700"
                >
                    Fichier visuel (MP4 ou GIF)
                </label>
                <input
                    id="video"
                    type="file"
                    accept="video/mp4,image/gif"
                    class="input w-full preset-outline-surface-50-900"
                    on:change={onVideoChange}
                    required
                    disabled={isLoading}
                />
                {#if videoFile}
                    <p class="text-xs text-surface-500">
                        Sélectionné : {videoFile.name}
                    </p>
                {/if}
            </div>

            <div class="space-y-2 text-left">
                <label
                    for="parts"
                    class="block text-sm font-medium text-surface-700"
                >
                    Nombre de vidéos à générer
                </label>
                <div class="flex items-center gap-3">
                    <input
                        id="parts"
                        type="range"
                        min={minParts}
                        max={maxParts}
                        bind:value={parts}
                        class="range flex-1 accent-primary-500"
                        disabled={isLoading}
                    />
                    <span
                        class="badge preset-filled-primary-500-50 text-sm font-semibold"
                    >
                        {parts}
                    </span>
                </div>
                <p class="text-xs text-surface-500">
                    Choisis entre {minParts} et {maxParts} segments.
                </p>
            </div>

            <div class="pt-2 space-y-2">
                <button
                    type="submit"
                    class="btn btn-primary w-full flex items-center justify-center gap-2"
                    disabled={isLoading}
                >
                    {#if isLoading}
                        <span
                            class="h-4 w-4 border-2 border-surface-50 border-t-transparent rounded-full animate-spin"
                        />
                        <span>Génération en cours...</span>
                    {:else}
                        <span>Générer les vidéos</span>
                    {/if}
                </button>

                {#if isLoading}
                    <p class="text-xs text-center text-surface-500">
                        Le traitement peut prendre un peu de temps selon la
                        taille des fichiers.
                    </p>
                {/if}
            </div>
        </form>
    </section>
</main>
