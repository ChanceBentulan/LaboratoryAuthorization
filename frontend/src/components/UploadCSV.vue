<template>
    <v-card
        width="500px"
        max-width="500px"
        title="Upload Class Schedule CSV"
        subtitle="Upload the ismis csv file here"
      >
        <v-card-item>
            <v-file-input
                v-model="file"
                label="File input"
                counter
                show-size
                accept=".csv"
            />
        </v-card-item>
        <template v-slot:actions>
          <v-btn
            class="ms-auto"
            text="Upload"
            @click="uploadFile"
          ></v-btn>
        </template>
      </v-card>
</template>

<script>
import { mapActions } from 'vuex';

export default {
    name: 'UploadCSV',

    data() {
        return {
            file: null,
        };
    },

    methods: {
        ...mapActions(['uploadCSVFile']),

        async uploadFile() {
            const formData = new FormData();
            formData.append('file', this.file[0]);

            let response = await this.uploadCSVFile(formData);
            this.$emit('done-upload', response)
        }
    }
}
</script>