local module = std.extVar('module');
local pipeline = std.extVar('pipeline');

local sponnet = import '../../../sponnet/pipeline.libsonnet';

local dockerImage = module.name + '-docker-image';
local helmChart = module.name + '-helm-chart';

local moniker = sponnet.moniker(module.name);
local namespace = pipeline.namespace;

# Docker image 
local dockerArtifact = sponnet.artifacts
    .dockerImage()
    .withName('docker.io/' + module.properties.docker)
    .withReference('docker.io/' + module.properties.docker)
    .withArtifactAccount('docker-registry');

local expectedDocker = sponnet.expectedArtifact(dockerImage)
    .withMatchArtifact(dockerArtifact)
    .withUseDefaultArtifact(false)
    .withUsePriorArtifact(true);

# Chart
local helmArtifact = sponnet.artifacts
    .helmChart()
    .withName(module.properties.helm)
    .withReference(module.properties.helm)
    .withArtifactAccount('my-account');

local expectedHelm = sponnet.expectedArtifact(helmChart)
    .withDefaultArtifact(helmArtifact)
    .withMatchArtifact(helmArtifact)
    .withUseDefaultArtifact(true)
    .withUsePriorArtifact(true);

# Baked Manifest
local bakedManifest = sponnet.artifacts
    .embeddedBase64()
    .withArtifactAccount('embedded-artifact')
    .withName(helmChart + '-baked')
    .withKind('base64');

local expectedBakedManifest = sponnet.expectedArtifact(helmChart + '-baked')
                                     .withMatchArtifact(bakedManifest);


# Triggers
local dockerTrigger = sponnet.triggers
    .docker('Docker Trigger')
    .withExpectedArtifacts([expectedDocker])
    .withAccount("docker-io")
    .withRegistry("docker.io")
    .withRepository(module.properties.docker)
    .withTag('\\d+\\.\\d+\\.\\d+\\.');

# Stages
local bakeManifest = sponnet.stages
                     .bakeManifest('Bake')
                     .withReleaseOutputName('release')
                     .withNamespace(namespace)
                     .withTemplateArtifact(sponnet.inputArtifact(expectedHelm.id).fromAccount("helm-account"))
                     .withExpectedArtifacts([expectedBakedManifest]);

local trafficManagement = sponnet.trafficManagement()
                                 .withEnableTraffic(true)
                                 .withNamespace(namespace)
                                 .withServices('service ' + module.properties.serviceName)
                                 .withStrategy('highlander');

local deployManifest = sponnet.stages
                       .deployManifest('Deploy')
                       .withAccount(pipeline.properties.account)
                       .withManifestArtifact(expectedBakedManifest)
                       .withRequiredArtifactIds([expectedDocker])
                       .withMoniker(moniker)
                       .withTrafficManagement(trafficManagement)
                       .withRequisiteStages(bakeManifest)
                       .withSkipExpressionEvaluation();

sponnet.pipeline()
    .withApplication(module.name)
    .withId('deploy-' + module.name + '-' + namespace)
    .withName('Release ' + std.asciiUpper(namespace) + '-Alpha')
    .withExpectedArtifacts([expectedDocker, expectedHelm])
    .withTriggers([dockerTrigger])
    .withStages([bakeManifest, deployManifest])