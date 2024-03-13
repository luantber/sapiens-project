from google.cloud import aiplatform

job = aiplatform.PipelineJob(
    display_name="training_pipeline",
    template_path="pipeline/pipeline.yaml",
    parameter_values={"dataset_uri": "/gcs/sapiens_dataset/iris.csv"},
)


job.submit()
