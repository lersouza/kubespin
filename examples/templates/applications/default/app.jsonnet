local sponnet = import '../../../sponnet/application.libsonnet';
local module = std.extVar('module');

local contactEmail = if std.objectHas(module, 'contact') then module.contact else 'nomail@email.com';
local appDescription = if std.objectHas(module, 'description') then module.description else '';


sponnet.application()
    .withName(module.name)
    .withEmail(contactEmail)
    .withDescription(appDescription)