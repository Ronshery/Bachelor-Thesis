<template>
  <TabContentCardsWrapper>
    <TabContentCard>
      <template v-slot:title> Latency </template>
      <ApexBarChart />
    </TabContentCard>
  </TabContentCardsWrapper>
</template>

<script setup lang="ts">
import ApexBarChart from "@/components/utils/ApexBarChart.vue";
import TabContentCard from "@/components/NodePanel/tabContents/TabContentCard.vue";
import TabContentCardsWrapper from "@/components/NodePanel/tabContents/TabContentCardsWrapper.vue";
</script>

<style scoped></style>
