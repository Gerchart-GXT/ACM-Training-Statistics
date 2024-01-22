<template>
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
        <div class="container">
            <a class="navbar-brand" href="https://hhuacm.github.io">
                <img src="https://avatars.githubusercontent.com/u/153970098?s=40&v=4" alt="HHU-ACM-Training-Record" width="30" height="30">
            </a>
            <a class="navbar-brand link-primary link-underline-opacity-100-hove" href="https://hhuacm.github.io">HHU-ACM-Training-Record</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarText"
                aria-controls="navbarText" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse text-center" id="navbarText">
                <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                    <li class="nav-item">
                        <router-link class="nav-link" :to="{ name: 'Overview' }">Overview</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link class="nav-link" :to="{ name: 'CodeforcesMember' }">Codeforces</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link class="nav-link" :to="{ name: 'Members' }">Members</router-link>
                    </li>
                </ul>
                <!-- <ul class="navbar-nav" v-if="!$store.state.user.is_login">
                    <li class="nav-item">
                        <router-link class="nav-link" :to="{ name: 'LoginView' }">Login</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link class="nav-link" :to="{ name: 'RegisterView' }">Register</router-link>
                    </li>
                </ul>
                <ul class="navbar-nav" v-else>
                    <li class="nav-item">
                        <router-link class="nav-link" :to="{ name: 'userprofile', params: { userId: $store.state.user.id } }">
                            {{ $store.state.user.username }}
                        </router-link>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" style="cursor: pointer" @click="logout">退出</a>
                    </li>
                </ul> -->
            </div>
        </div>
    </nav>
</template>

<script>
export default {
    name: "NavBar",
    setup() {
        // const store = useStore();
        // const logout = () => {
        //     store.commit('logout');
        // };

        // return {
        //     logout,
        // }
    }
}
</script>

<style scoped></style>
    