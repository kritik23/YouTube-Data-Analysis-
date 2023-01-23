import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

from awsglue.dynamicframe import DynamicFrame

args = getResolvedOptions(sys.argv, ["JOB_NAME"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

predicate_pushdown = "region in ('ca','gb','us')"

# Script generated for node AWS Glue Data Catalog
AWSGlueDataCatalog_node1674432670686 = glueContext.create_dynamic_frame.from_catalog(
    database="youtube_raw",
    table_name="raw_statistics",
    transformation_ctx="AWSGlueDataCatalog_node1674432670686",
    push_down_predicate = predicate_pushdown,
)

# Script generated for node Change Schema (Apply Mapping)
ChangeSchemaApplyMapping_node1674432691621 = ApplyMapping.apply(
    frame=AWSGlueDataCatalog_node1674432670686,
    mappings=[
        ("video_id", "string", "video_id", "string"),
        ("trending_date", "string", "trending_date", "string"),
        ("title", "string", "title", "string"),
        ("channel_title", "string", "channel_title", "string"),
        ("category_id", "long", "category_id", "long"),
        ("publish_time", "string", "publish_time", "string"),
        ("tags", "string", "tags", "string"),
        ("views", "long", "views", "long"),
        ("likes", "long", "likes", "long"),
        ("dislikes", "long", "dislikes", "long"),
        ("comment_count", "long", "comment_count", "long"),
        ("thumbnail_link", "string", "thumbnail_link", "string"),
        ("comments_disabled", "boolean", "comments_disabled", "boolean"),
        ("ratings_disabled", "boolean", "ratings_disabled", "boolean"),
        ("video_error_or_removed", "boolean", "video_error_or_removed", "boolean"),
        ("description", "string", "description", "string"),
        ("region", "string", "region", "string"),
    ],
    transformation_ctx="ChangeSchemaApplyMapping_node1674432691621",
)
resolvechoice2 = ResolveChoice.apply(frame = ChangeSchemaApplyMapping_node1674432691621, choice = "make_struct", transformation_ctx = "resolvechoice2")

dropnullfields3 = DropNullFields.apply(frame = resolvechoice2, transformation_ctx = "dropnullfields3")

datasink1 = dropnullfields3.toDF().coalesce(1)
df_final_output = DynamicFrame.fromDF(datasink1, glueContext, "df_final_output")
# Script generated for node Amazon S3
AmazonS3_node1674432697293 = glueContext.write_dynamic_frame.from_options(
    frame=ChangeSchemaApplyMapping_node1674432691621,
    connection_type="s3",
    format="glueparquet",
    connection_options={
        "path": "s3://youtube-dev-useast-1-2303-cleansed/youtube/raw_statistics/",
        "partitionKeys": ["region"],
    },
    transformation_ctx="AmazonS3_node1674432697293",
)


job.commit()
