<script lang="ts">
    import "./layout.css";
    import recompo from "$lib/assets/recompo.png";

    let { children } = $props();
</script>

<svelte:head>
    <link rel="icon" type="image/png" href={recompo} />
</svelte:head>

{@render children()}
